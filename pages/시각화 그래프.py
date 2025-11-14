import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="치킨 판매량 시각화", layout="wide")

st.title("🍗 월별 치킨 판매량 분석")

# 샘플 데이터 생성 (2024년 월별 판매량)
months = ['1월', '2월', '3월', '4월', '5월', '6월', 
          '7월', '8월', '9월', '10월', '11월', '12월']
sales = [450, 520, 480, 650, 720, 800, 
         950, 890, 720, 580, 650, 850]

df = pd.DataFrame({
    '월': months,
    '판매량(개)': sales
})

# 통계 정보 표시
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("총 판매량", f"{sum(sales):,}개")
with col2:
    st.metric("평균 판매량", f"{sum(sales)//len(sales):,}개")
with col3:
    st.metric("최대 판매량", f"{max(sales):,}개")
with col4:
    st.metric("최소 판매량", f"{min(sales):,}개")

st.divider()

# 탭을 이용한 여러 그래프 표시
tab1, tab2, tab3, tab4 = st.tabs(["📊 꺾은선 그래프", "📈 막대 그래프", "🔵 영역 그래프", "🎯 조합 그래프"])

# 1. 꺾은선 그래프
with tab1:
    fig_line = px.line(df, x='월', y='판매량(개)', 
                       title='월별 치킨 판매량 추이',
                       markers=True,
                       template='plotly_white')
    fig_line.update_traces(line=dict(width=3, color='#FF6B6B'),
                           marker=dict(size=10))
    fig_line.update_layout(hovermode='x unified', height=500)
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.info("💡 꺾은선 그래프는 시간에 따른 판매량의 변화 추이를 명확하게 보여줍니다.")

# 2. 막대 그래프
with tab2:
    fig_bar = px.bar(df, x='월', y='판매량(개)',
                     title='월별 치킨 판매량 비교',
                     color='판매량(개)',
                     color_continuous_scale='Reds',
                     template='plotly_white')
    fig_bar.update_layout(hovermode='x unified', height=500)
    fig_bar.update_xaxes(tickangle=0)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.info("💡 막대 그래프는 각 월별 판매량을 직관적으로 비교할 수 있습니다.")

# 3. 영역 그래프
with tab3:
    fig_area = px.area(df, x='월', y='판매량(개)',
                       title='월별 누적 판매량 변화',
                       template='plotly_white')
    fig_area.update_traces(fillcolor='rgba(255, 107, 107, 0.4)',
                           line=dict(color='#FF6B6B', width=2))
    fig_area.update_layout(hovermode='x unified', height=500)
    st.plotly_chart(fig_area, use_container_width=True)
    
    st.info("💡 영역 그래프는 판매량의 누적 변화를 시각화합니다.")

# 4. 조합 그래프 (막대 + 꺾은선)
with tab4:
    fig_combo = go.Figure()
    
    # 막대 그래프
    fig_combo.add_trace(go.Bar(x=df['월'], y=df['판매량(개)'],
                               name='판매량',
                               marker_color='rgba(255, 107, 107, 0.6)'))
    
    # 꺾은선 그래프
    fig_combo.add_trace(go.Scatter(x=df['월'], y=df['판매량(개)'],
                                   name='추이선',
                                   mode='lines+markers',
                                   line=dict(color='#FF6B6B', width=3),
                                   marker=dict(size=8)))
    
    fig_combo.update_layout(
        title='월별 치킨 판매량 (조합 차트)',
        xaxis_title='월',
        yaxis_title='판매량(개)',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    st.plotly_chart(fig_combo, use_container_width=True)
    
    st.info("💡 조합 그래프는 막대와 꺾은선을 함께 사용하여 데이터를 다각도로 분석합니다.")

st.divider()

# 데이터 테이블 표시
st.subheader("📋 판매량 데이터")
st.dataframe(df, use_container_width=True)

# 월별 성장률 계산
st.subheader("📈 월별 성장률")
growth_rate = []
for i in range(len(sales)):
    if i == 0:
        growth_rate.append("초기")
    else:
        rate = ((sales[i] - sales[i-1]) / sales[i-1] * 100)
        growth_rate.append(f"{rate:+.1f}%")

df['성장률'] = growth_rate
st.dataframe(df, use_container_width=True)

# 인사이트
st.subheader("💡 주요 인사이트")
col1, col2 = st.columns(2)

with col1:
    max_month = months[sales.index(max(sales))]
    st.success(f"최고 판매 월: {max_month} ({max(sales)}개)")
    
with col2:
    min_month = months[sales.index(min(sales))]
    st.warning(f"최저 판매 월: {min_month} ({min(sales)}개)")
