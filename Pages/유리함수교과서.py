import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Poly, fraction, solve, apart, limit, oo
from sympy.parsing.mathematica import parse_mathematica
from sympy.abc import x # SymPy 변수 'x'를 사용합니다.

# ==============================================================================
# 함수 정의: 유리함수의 성질 분석
# ==============================================================================

def analyze_rational_function(poly_n, poly_d):
    """
    분자, 분모 다항식을 받아 유리함수의 성질을 분석합니다.
    Args:
        poly_n (SymPy Poly): 분자 다항식
        poly_d (SymPy Poly): 분모 다항식
    Returns:
        dict: 분석 결과
    """
    n_degree = poly_n.degree()
    d_degree = poly_d.degree()

    # 1. 수직 점근선 (Vertical Asymptote, VA)
    # 분모가 0이 되는 x값
    va_candidates = solve(poly_d.as_expr(), x)
    # 분모와 분자가 동시에 0이 되지 않는 근만 수직 점근선입니다.
    # SymPy simplify와 subs를 사용하여 hole이 아닌지 확인합니다.
    # 간단한 유리식으로 가정하고, 분모=0인 지점을 VA로 설정합니다.
    # 더 복잡한 경우(공통 인수) 처리는 필요에 따라 추가될 수 있습니다.
    vertical_asymptotes = [val for val in va_candidates if (poly_n.subs(x, val) != 0)]
    
    # 2. 수평 점근선 (Horizontal Asymptote, HA)
    if n_degree < d_degree:
        # 분자 차수 < 분모 차수 -> y = 0
        horizontal_asymptote = "y = 0"
    elif n_degree == d_degree:
        # 분자 차수 = 분모 차수 -> y = (최고차항 계수의 비)
        a_n = poly_n.LC()  # Leading Coefficient
        b_d = poly_d.LC()
        ha_value = a_n / b_d
        horizontal_asymptote = f"y = {ha_value:.3f}" if ha_value != int(ha_value) else f"y = {int(ha_value)}"
    else: # n_degree > d_degree
        # 분자 차수 > 분모 차수 -> 수평 점근선 없음 (사선/곡선 점근선 존재 가능)
        horizontal_asymptote = "없음 (사선/곡선 점근선 존재 가능)"
    
    # 3. 정의역 (Domain)
    domain_exclusions = [str(val) for val in va_candidates]
    if domain_exclusions:
        domain = f"$\{x | x \in \mathbb{{R}}, x \neq {', '.join(domain_exclusions)}\}$"
    else:
        domain = "$\{x | x \in \mathbb{{R}}\}$ (모든 실수)"

    # 4. 치역 (Range)
    # 간단한 형태 (1/x, (ax+b)/(cx+d))에 대해 수평 점근선 값만 제외하는 것으로 단순화
    # 더 복잡한 치역 계산은 극점 및 그래프 분석이 필요합니다.
    if horizontal_asymptote.startswith("y = "):
        ha_val = horizontal_asymptote.replace("y = ", "")
        try:
            ha_num = float(ha_val)
            range_text = f"$\{y | y \in \mathbb{{R}}, y \neq {ha_num:.3f}\}$"
        except ValueError:
             range_text = "복잡한 계산이 필요하거나 SymPy로 단순화하기 어려움"
    else:
        range_text = "수평 점근선이 없으므로 복잡한 계산이 필요함"


    # 5. 대칭성 (Symmetry)
    # 원점 대칭 (기함수): f(-x) = -f(x)
    # y축 대칭 (우함수): f(-x) = f(x)
    # 유리함수 형태에 따라 대칭의 중심이 달라집니다. 여기서는 원점/y축 대칭만 간단히 확인.
    f_x = poly_n.as_expr() / poly_d.as_expr()
    f_neg_x = f_x.subs(x, -x)
    
    symmetry = "없음"
    if f_neg_x == f_x:
        symmetry = "y축 대칭 (우함수)"
    elif f_neg_x == -f_x:
        symmetry = "원점 대칭 (기함수)"
    # 평행이동된 유리함수 (y=(ax+b)/(cx+d) 형태)의 점 대칭 중심 계산
    if d_degree == 1 and n_degree <= 1:
        # f(x) = (ax+b)/(cx+d) 형태의 경우, 대칭 중심은 (VA, HA)의 교점
        if len(vertical_asymptotes) == 1 and horizontal_asymptote.startswith("y = "):
            va_val = float(vertical_asymptotes[0])
            ha_val = float(horizontal_asymptote.replace("y = ", ""))
            symmetry = f"점 ({va_val:.3f}, {ha_val:.3f})에 대해 점대칭"

    # 6. 사선 점근선 (Slant Asymptote)
    slant_asymptote = "없음"
    if n_degree == d_degree + 1:
        # 분자 차수가 분모 차수보다 1 클 경우 (긴 나눗셈 수행)
        try:
            quotient, remainder = poly_n.as_expr().as_poly().div(poly_d.as_expr().as_poly())
            slant_asymptote = f"y = {quotient}"
        except Exception:
            slant_asymptote = "계산 오류"
    

    return {
        "유리식": str(poly_n.as_expr() / poly_d.as_expr()),
        "수직 점근선 (VA)": [f"x = {val:.3f}" if val != int(val) else f"x = {int(val)}" for val in vertical_asymptotes],
        "수평 점근선 (HA)": horizontal_asymptote,
        "사선 점근선 (SA)": slant_asymptote,
        "정의역": domain,
        "치역 (단순화)": range_text,
        "대칭성": symmetry,
    }

# ==============================================================================
# 함수 정의: 그래프 그리기
# ==============================================================================

def plot_rational_function(poly_n, poly_d, va_lines, ha_line, sa_line):
    """
    유리함수의 그래프와 점근선을 그립니다.
    """
    # 분모가 0이 되는 지점 찾기
    va_candidates = solve(poly_d.as_expr(), x)
    va_points = [float(val) for val in va_candidates if val.is_real] # 실수 근만 사용

    # 그래프 범위 설정
    x_min, x_max = -5, 5
    y_min, y_max = -10, 10
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # VA 지점을 기준으로 도메인을 분할
    plot_points = [x_min] + sorted([p for p in va_points if x_min < p < x_max]) + [x_max]
    
    # 2.3의 팁을 참고하여 VA 근처를 피해서 그래프를 그립니다.
    epsilon = 0.01 
    
    for i in range(len(plot_points) - 1):
        start = plot_points[i]
        end = plot_points[i+1]
        
        # VA 근처를 피하기
        if start in va_points: start += epsilon
        if end in va_points: end -= epsilon
        
        if start >= end: continue # 유효하지 않은 구간 건너뛰기

        # x 값 생성 (VA 근처에서 더 많은 점을 찍기 위해 linspace 사용)
        x_vals = np.linspace(start, end, 500)
        
        # y 값 계산
        try:
            # SymPy 표현식을 numpy 함수로 변환 (속도 향상 및 분수 계산)
            func = np.vectorize(lambda val: float(poly_n.subs(x, val) / poly_d.subs(x, val)))
            y_vals = func(x_vals)

            # 너무 큰 값(무한대에 가까운)을 잘라내어 그래프가 보기 좋게 함
            y_vals[y_vals > y_max] = np.nan 
            y_vals[y_vals < y_min] = np.nan
            
            ax.plot(x_vals, y_vals, label=f"Rational Function", color='blue')
        except Exception:
            # 계산 오류 발생 시 해당 구간 건너뛰기
            continue

    # ==================================
    # 점근선 그리기
    # ==================================
    # 1. 수직 점근선 (VA)
    for va in va_lines:
        try:
            val = float(va.split('=')[1].strip())
            ax.axvline(val, color='red', linestyle='--', linewidth=1, label='VA' if val == va_points[0] else None)
        except:
            continue

    # 2. 수평 점근선 (HA)
    if ha_line.startswith("y = "):
        try:
            val = float(ha_line.split('=')[1].strip())
            ax.axhline(val, color='green', linestyle='--', linewidth=1, label='HA')
        except:
            pass

    # 3. 사선 점근선 (SA)
    if sa_line.startswith("y = "):
        try:
            # 사선 점근선은 SymPy의 parse_mathematica로 다시 표현식으로 변환하여 그립니다.
            sa_expr = parse_mathematica(sa_line.split('=')[1].strip(), mapping={'x': x})
            x_range = np.linspace(x_min, x_max, 50)
            
            # SymPy 표현식을 numpy 함수로 변환
            sa_func = np.vectorize(lambda val: float(sa_expr.subs(x, val)))
            y_sa_vals = sa_func(x_range)
            
            ax.plot(x_range, y_sa_vals, color='orange', linestyle=':', linewidth=1, label='SA')
        except Exception as e:
            # st.error(f"사선 점근선 그리기 오류: {e}") # 디버깅용
            pass


    # ==================================
    # 그래프 설정
    # ==================================
    ax.set_title(f"유리함수 $y = f(x)$ 그래프")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.legend(loc='upper left')
    
    st.pyplot(fig)
    

[Image of Rational function graph with asymptotes]
 # 그래프와 점근선 다이어그램 태그

# ==============================================================================
# Streamlit 앱 본문
# ==============================================================================

st.set_page_config(
    page_title="유리함수 교과서 앱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 유리함수 마스터 교과서 앱")
st.markdown("""
이 앱은 사용자가 입력한 유리함수 $y = \frac{P(x)}{Q(x)}$의 **성질을 요약하고 그래프를 시각화**하여 학습을 돕습니다.
""")

st.sidebar.header("함수 입력")

# 함수 입력 (SymPy가 처리할 수 있도록 문자열로 입력 받음)
function_str = st.sidebar.text_input(
    "유리 함수를 $\\frac{\\text{분자}}{\\text{분모}}$ 형태로 입력하세요. (예: (x+2)/(x-1))",
    value="(x+2)/(x-1)"
)

# SymPy로 분자와 분모 추출
try:
    # 괄호 처리를 위해 SymPy의 fraction을 사용
    expr = parse_mathematica(function_str, mapping={'x': x})
    num_expr, den_expr = fraction(expr)
    
    # 분자/분모 다항식 객체 생성
    poly_n = Poly(num_expr, x)
    poly_d = Poly(den_expr, x)
    
    if poly_d.degree() == 0 and poly_d.LC() == 0:
        # 분모가 0인 경우 (예: 1/0)
        st.error("**오류:** 분모가 0이 될 수 없습니다. 올바른 유리 함수를 입력해 주세요.")
    else:
        # ==============================================================
        # 1. 성질 분석 및 요약
        # ==============================================================
        st.header("📊 유리함수의 성질 요약")

        analysis_result = analyze_rational_function(poly_n, poly_d)

        # 분석 결과를 마크다운으로 깔끔하게 정리
        st.markdown(f"**대상 함수:** $y = {analysis_result['유리식']}$")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 핵심 성질")
            st.markdown(f"* **정의역 (Domain):** {analysis_result['정의역']}")
            st.markdown(f"* **치역 (Range) (단순화):** {analysis_result['치역 (단순화)']}")
            st.markdown(f"* **대칭성:** {analysis_result['대칭성']}")

        with col2:
            st.subheader("📈 점근선")
            st.markdown(f"* **수직 점근선 (VA):** {', '.join(analysis_result['수직 점근선 (VA)'])}")
            st.markdown(f"* **수평 점근선 (HA):** {analysis_result['수평 점근선 (HA)']}")
            st.markdown(f"* **사선 점근선 (SA):** {analysis_result['사선 점근선 (SA)']}")
            
        st.divider()

        # ==============================================================
        # 2. 그래프 시각화
        # ==============================================================
        st.header("📉 그래프 변화 및 시각화")
        
        st.markdown("함수의 그래프와 점근선을 표시합니다.")
        plot_rational_function(
            poly_n, 
            poly_d, 
            analysis_result['수직 점근선 (VA)'], 
            analysis_result['수평 점근선 (HA)'], 
            analysis_result['사선 점근선 (SA)']
        )
        
        # ==============================================================
        # 3. 추가 학습 (부분분수 분해를 통한 평행이동 이해)
        # ==============================================================
        st.subheader("💡 평행 이동 관점 (부분분수 분해)")
        
        if poly_d.degree() == 1 and poly_n.degree() == 1:
            try:
                # f(x) = k/(x-p) + q 형태로 변형
                partial_fraction = apart(expr, x)
                st.markdown(f"부분분수 분해 결과: $y = {partial_fraction}$")
                st.info(f"""
                이 형태는 기본 함수 $y = \\frac{{k}}{{x}}$를 x축 방향으로 **$p$** 만큼, y축 방향으로 **$q$** 만큼 평행 이동한 형태로 해석할 수 있습니다.
                * VA: $x = p$
                * HA: $y = q$
                """)
            except Exception:
                st.info("부분분수 분해가 단순하지 않아 해석이 어렵습니다.")
        else:
            st.info("차수가 높아 단순한 평행 이동 형태로 해석하기 어렵거나, 부분분수 분해가 필요하지 않은 형태입니다.")


except Exception as e:
    st.error(f"**오류:** 함수를 해석할 수 없습니다. 입력 형식이 올바른지 확인해 주세요. (예: (2*x+1)/(x-3))")
    # st.error(f"디버깅 정보: {e}") # 개발자를 위한 에러 메시지
