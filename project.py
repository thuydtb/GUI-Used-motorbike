import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import joblib, json
import datetime
import streamlit.components.v1 as components



# --- CSS thêm màu nền ---
st.markdown("""
<style>
/* Tablist giãn đều */
[data-testid="stTabs"] [role="tablist"] {
    display: flex !important;
    justify-content: space-between !important;
}

/* Tab chung */
[data-testid="stTabs"] [role="tab"] {
    flex: 1 !important;
    text-align: center !important;
    color: white !important;   /* màu chữ mặc định */
    border: none !important;
    background: transparent !important;
}

/* Màu chữ mặc định */
[data-testid="stTabs"] [role="tab"] p {
    color: white !important;
}

/* Tab được chọn: đổi màu chữ */
[data-testid="stTabs"] [role="tab"][aria-selected="true"] p {
    color: #0ea5e9 !important;
    font-weight: bold !important;
}

       
/* Background toàn bộ trang */
.stApp {
    background-color: #0f172a ;
}

/* Đổi màu nền sidebar */
[data-testid="stSidebar"] {
    background-color: #e5e7eb; 
}
            
/* Màu chữ */
h1 {
    color: #e2e8f0 !important;
}
h2 {
    color: #0ea5e9 !important;
    font-size: 3.5rem !important;
}
         
p {
    color: #94a3b8 ;
    font-size: 1.3rem !important;
}
img:hover {
    transform: scale(1.05);        /* phóng to nhẹ */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    filter: brightness(1.1);       /* tăng sáng nhẹ */
    cursor: pointer;               /* đổi con trỏ */
    box-shadow: 0 8px 20px rgba(14,165,233,0.6); /* đổ bóng xanh */
}
/* Nút mặc định */
div.stButton > button:first-child {
    background-color: #0ea5e9;   /* nền xanh */
    color: white !important;     /* chữ trắng */
    border: none;
    padding: 0.6em 1.2em;
    border-radius: 6px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

/* Đảm bảo chữ bên trong (p, span) cũng trắng */
div.stButton > button:first-child * {
    color: white !important;
}

/* Hover */
div.stButton > button:first-child:hover {
    background-color: #f43f5e;   /* nền khi hover */
    color: white !important;     /* chữ vẫn trắng */
}
div.stButton > button:first-child:hover * {
    color: white !important;
}


</style>
""", unsafe_allow_html=True)

# Using menu
st.image("banner.png")
st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs([
    "Thông tin dự án",
    "Thuật toán sử dụng",
    "Dự báo giá",
    "Phát hiện bất thường"
])


# Thêm text hiển thị cố định ở sidebar
st.sidebar.markdown('### 🧑‍💻 Thành viên thực hiện')
st.sidebar.write("- Dương Hoàng Phúc\n- Đinh Thị Bích Thủy")

st.sidebar.markdown('### 🎓 GVHD')
st.sidebar.write("- Khuất Thùy Phương")

st.sidebar.markdown('### 📅 Ngày thuyết trình')
st.sidebar.write("- 22/11/2025")


st.markdown('<div class="main-content">', unsafe_allow_html=True)


# ===================  PHẦN NỘI DUNG MENU ===================
with tab1:  
    st.markdown("""
    <h2 style="text-align:center; margin-bottom:10px;">
        Tổng quan dự án
    </h2>
    <hr style="border:2px solid white; width:200px; margin:0 auto;margin-bottom:30px;">
    """, unsafe_allow_html=True)

    st.markdown("""
<p style="text-align:center; margin-left:100px; margin-right:100px;margin-bottom:30px;">
    Chợ Tốt là một trong những sàn thương mại điện tử hàng đầu tại Việt Nam, chuyên về bất động sản, ô tô, xe máy và nhiều dịch vụ khác. 
    Dự án này tập trung vào thị trường xe máy cũ và bao gồm hai chủ đề chính:
</p>

""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.image("Topic1.png")
    with col2:
        st.image("Topic2.png")

    st.markdown("""
        <h2 style="text-align:center; margin-top:60px;">
            Phân tích dữ liệu
        </h2>
        <hr style="border:2px solid white; width:200px; margin:0 auto;margin-bottom:30px;">
    """, unsafe_allow_html=True)

    # Top 5 Most Listed Motorbikes
    df = pd.read_csv("cleaned_motobikes_data.csv")
    top_models = df['model'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(8,4))
    fig.patch.set_facecolor("#1E293B")   # nền ngoài
    ax.set_facecolor("#1E293B")          # nền trong chart
    top_models.plot(kind='bar', ax=ax, color="#0ea5e9")
    ax.tick_params(colors="white")
    ax.set_title("Top 5 Most Listed Motorbikes",color="white",  family="Arial",weight="bold")
    ax.set_xlabel("") 
    ax.set_ylabel("Number of Records",color="white")

    # Tree map
    brand_counts = df['brand'].value_counts().reset_index()
    brand_counts.columns = ['brand', 'count']
    custom_scale = [
        [0, "#bae6fd"],   # xanh rất nhạt
        [0.5, "#0ea5e9"], # màu gốc
        [1, "#0284c7"]    # xanh đậm hơn
    ]
    fig1 = go.Figure(go.Treemap(
        labels=brand_counts['brand'],
        values=brand_counts['count'],
        parents=[""] * len(brand_counts),
        marker=dict(
            colors=brand_counts['count'],
            colorscale=custom_scale,
            line=dict(color="#1E293B", width=0)
        ),
        text=[f"{c}" for  c in  brand_counts['count']],
        textfont=dict(color="white"),
        hovertemplate='<b>%{label}</b><br>Số lượng: %{value}<extra></extra>'

    ))
    fig1.update_layout(
        title="Motorbike Brand Distribution",
        title_font=dict(color="white",family="Arial"),
        height=400,
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(color="white"),
        template=None
    )


    # Chia màn hình thành 2 cột
    st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1],gap="large")  
    with col1:
        st.pyplot(fig)              
    with col2:
        st.plotly_chart(fig1, width="stretch")

    # Boxplot Distribution
    st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
    fig, axes = plt.subplots(1, 3, figsize=(12,4))
    # Boxplot cho km_driven
    axes[0].boxplot(df['km_driven'], patch_artist=True,
        boxprops=dict(facecolor="#0ea5e9"))
    axes[0].set_title("Kilometers Driven")
    # Boxplot cho age
    axes[1].boxplot(df['age'], patch_artist=True,
        boxprops=dict(facecolor="#0ea5e9"))
    axes[1].set_title("Age")
    # Boxplot cho price
    axes[2].boxplot(df['price'], patch_artist=True,
        boxprops=dict(facecolor="#0ea5e9"))
    axes[2].set_title("Price")
    plt.tight_layout()
    st.pyplot(fig)
    
    #Listings by Location
    top10_locations = df['location'].value_counts().head(10)
    fig2, ax = plt.subplots(figsize=(8,6))
    bars = ax.bar(top10_locations.index, top10_locations.values, color="#0ea5e9")
    ax.set_title("Top 10 Listings by Location", fontsize=14, color="#ffffff")
    ax.set_xlabel("")
    ax.set_ylabel("Number of Records", color="white")
    fig2.patch.set_facecolor("#1E293B")
    ax.set_facecolor("#1E293B")
    ax.tick_params(colors="white")
    plt.xticks(rotation=45, ha="right", color="white")
    plt.yticks(color="white")

    # Distribution of Vehicle Types
    vehicle_counts = df['vehicle_type'].value_counts()
    fig3, ax = plt.subplots(figsize=(6,4))
    colors = ["#f472b6", "#0ea5e9", "#22c55e", "#eab308", "#a855f7"]  # bảng màu tuỳ chọn
    ax.pie(vehicle_counts.values,
       labels=vehicle_counts.index,
       autopct="%1.1f%%",
       startangle=90,
       colors=colors,
       textprops={"color":"white", "fontsize":12})
    ax.set_title("Distribution of Vehicle Types", color="white", fontsize=12)
    ax.set_aspect('equal')
    fig3.patch.set_facecolor("#1E293B")
    ax.set_facecolor("#1E293B")

    # Chia màn hình thành 2 cột
    st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1],gap="large")  
    with col1:
        st.pyplot(fig2)              
    with col2:
        st.pyplot(fig3)

    # Wordcloud
    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
    st.image("wordcloud.png", width="stretch")


with tab2:
    st.markdown("""
    <h2 style="text-align:center; margin-bottom:10px;">
        1. Mô hình dự báo giá
    </h2>
    <hr style="border:2px solid white; width:200px; margin:0 auto;margin-bottom:30px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color:#ffffff;">
        Mục đích:
    </p>
    <p>
    Tính năng này cho phép người mua ước tính giá thị trường hợp lý của một chiếc xe máy cũ dựa trên nhu cầu cá nhân của họ.
    Bằng cách nhập các thông tin như hãng, dòng xe, loại xe, dung tích xi-lanh, số km đã đi, địa điểm và năm đăng ký, hệ thống sẽ tạo ra dự đoán giá chính xác bằng mô hình học máy.
    Điều này cung cấp cho người dùng một mức tham chiếu thực tế về giá của một chiếc xe máy phù hợp với sở thích của họ.
    </p>                
    <p style="color:#ffffff;">
        Các đặc trưng đầu vào:
    </p>        
    <ul style="color:#94a3b8; font-size:1.3rem;">
        <li>brand, model, vehicle_type, engine_capacity, origin, location, km_driven, age</li>
    </ul>
    <p style="color:#ffffff;">
        Các mô hình đã thử nghiệm::
    </p>        
    <ul style="color:#94a3b8; font-size:1.3rem;">
        <li>Linear Regression</li>
        <li>Decision Tree</li> 
        <li>Random Forest</li> 
        <li>Gradient Boosting</li> 
        <li>SVR</li>                        
    </ul>
    <p style="color:#ffffff;">
        Chọn thuật toán<span style="color:red;">SVR</span> vì cho R² cao nhất.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
    st.image("price_prediction.png")
    st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <h2 style="text-align:center; margin-bottom:10px;">
        2. Mô hình phát hiện bất thường
    </h2>
    <hr style="border:2px solid white; width:200px; margin:0 auto;margin-bottom:30px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color:#ffffff;">
        Mục đích:
    </p>
    <p>
    Hệ thống phát hiện bất thường xác định các tin rao giá bất thường hoặc đáng nghi trong thị trường xe máy cũ bằng cách kết hợp nhiều phương pháp khác nhau và tổng hợp kết quả qua mô hình ensemble có trọng số:
    </p>                
    """, unsafe_allow_html=True)
    st.markdown("""
<h3 style="color:#0ea5e9;">I. Business Rules (Trọng số: 0.1)</h3>
<ul style="color:#94a3b8; font-size:1.1rem;">
    <li>Giá bất thường: Xe có giá &lt;1 triệu VND (bait pricing) hoặc &gt;500 triệu VND được đánh dấu.</li>
    <li>Dung tích động cơ vs Giá: Xe &lt;175cc nhưng giá &gt;500 triệu VND được coi là bất thường.</li>
    <li>Số km đã đi: Xe có số km &gt;200.000 km được đánh dấu.</li>
</ul>

<h3 style="color:#0ea5e9;">II. Modified Z-score (Trọng số: 0.1)</h3>
<ul style="color:#94a3b8; font-size:1.1rem;">
    <li>Phát hiện giá bất thường dựa trên median, giảm ảnh hưởng của các giá trị cực đoan.</li>
    <li>Hạn chế: chỉ xét riêng giá, cần kết hợp với các phương pháp khác.</li>
</ul>

<h3 style="color:#0ea5e9;">III. Phương pháp IQR (Trọng số: 0.1)</h3>
<ul style="color:#94a3b8; font-size:1.1rem;">
    <li>Sử dụng phân vị (percentile) để phát hiện bất thường, phù hợp với tập dữ liệu có nhiều outlier.</li>
</ul>

<h3 style="color:#0ea5e9;">IV. Isolation Forest (Trọng số: 0.4)</h3>
<ul style="color:#94a3b8; font-size:1.1rem;">
    <li>Xét nhiều đặc trưng cùng lúc (giá, tuổi xe, số km).</li>
    <li>Phát hiện các kết hợp bất thường (ví dụ: xe mới + km cao + giá thấp).</li>
    <li>Không bị ảnh hưởng bởi outlier cực đoan; nhạy với các giá trị km bị giả mạo.</li>
</ul>

<h3 style="color:#0ea5e9;">V. Dự đoán dựa trên Residual (Trọng số: 0.3)</h3>
<ul style="color:#94a3b8; font-size:1.1rem;">
    <li>Dự đoán giá kỳ vọng bằng mô hình và đánh dấu các sai lệch lớn là bất thường.</li>
</ul>

<h3 style="color:#0ea5e9;">Tổng hợp điểm bất thường (Ensemble)</h3>
<p style="color:#94a3b8; font-size:1.1rem;">
    Điểm bất thường = 0.1 × Business Rules + 0.1 × Modified Z-score + 0.1 × IQR + 
    0.4 × Isolation Forest + 0.3 × Residual.
</p>
<p style="color:#f472b6; font-size:1.2rem; font-weight:bold;">
    ➡️ Các tin rao vượt ngưỡng 0.5 được coi là bất thường.
</p>
""", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])  # chia đều 2 cột

    with col1:
        st.markdown("""
        <h3 style="color:#0ea5e9;">📊 Kết quả đánh giá trên tập dữ liệu</h3>
        <ul style="color:#94a3b8; font-size:1.1rem;">
            <li>Ngưỡng 0.3 → 1054 bất thường (14,77%)</li>
            <li>Ngưỡng 0.4 → 778 bất thường (10,90%)</li>
            <li>Ngưỡng 0.5 → 688 bất thường (9,64%)</li>
            <li>Ngưỡng 0.6 → 605 bất thường (8,48%)</li>
            <li>Ngưỡng 0.7 → 406 bất thường (5,69%)</li>
        </ul>

        <p style="color:#0ea5e9;">========== KẾT QUẢ ENSEMBLE (ngưỡng = 0.5) ==========</p>
        <p style="color:#ffffff;">
            Tổng số bất thường: 688<br>
            Tỷ lệ: 9,64%
        </p>
        """, unsafe_allow_html=True)

    with col2:
        st.image("Anomaly_Detection.png", width='stretch')

    st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
    
          
with tab3:
    st.markdown("""
    <h2 style="text-align:center; margin-bottom:10px;">
        Dự báo giá
    </h2>
    <hr style="border:2px solid white; width:200px; margin:0 auto;margin-bottom:30px;">
    """, unsafe_allow_html=True)

    st.markdown("""
<p style="color:#ffffff">
Vui lòng nhập đầy đủ các thông tin bên dưới trước khi thực hiện dự báo giá.
</p>

""", unsafe_allow_html=True)

    # Tạo điều khiển để người dùng nhập các thông tin về xe máy
    col1, col2 = st.columns(2,gap="large")
    with col1:
        thuong_hieu = st.selectbox("Hãng xe", df['brand'].sort_values().unique())
        dong_xe = st.selectbox("Dòng xe", df['model'].sort_values().unique())
        loai_xe = st.selectbox("Loại xe", df['vehicle_type'].sort_values().unique())
        nguon_goc = st.selectbox("Xuất xứ", df['origin'].sort_values().unique())

    with col2:
        dung_tich_xi_lanh = st.selectbox("Dung tích xi-lanh", df['engine_capacity'].sort_values().unique())
        nam_dang_ky = st.slider("Năm đăng ký", 1980, 2025, 2020)
        so_km_da_di = st.number_input("Số km đã đi", min_value=0, max_value=200000, value=50000, step=1000)
        quan = st.selectbox("Chọn quận của bạn", df['location'].sort_values().unique())

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    du_doan_gia = st.button("Thực hiện dự báo giá")

    model = joblib.load("best_model_SVR_20251122_142655.pkl")

    if du_doan_gia:
        # Chuẩn bị dữ liệu đầu vào
        input_data = pd.DataFrame({
            "brand": [thuong_hieu],
            "model": [dong_xe],
            "vehicle_type": [loai_xe],
            "origin": [nguon_goc],
            "engine_capacity": [dung_tich_xi_lanh],
            "age": [2025 - nam_dang_ky],
            "km_driven": [so_km_da_di],
            "location": [quan]
        })

        # Dự đoán giá
        predicted_price_log = model.predict(input_data)[0]
        predicted_price = np.expm1(predicted_price_log)
        predicted_price_vnd = predicted_price * 1_000_000
        formatted_price = f"{predicted_price_vnd:,.0f}"


        # In thông tin + kết quả
        st.markdown(f"""
        <div style="
            border:2px solid #0ea5e9;
            border-radius:8px;
            padding:15px;
            margin-top:15px;
            background-color:#1E293B;">
            <h4 style="color:#0ea5e9;">🛵 Thông tin bạn đã chọn:</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; color:#e2e8f0; font-size:1.1rem;">
                <ul style="list-style-type:disc; padding-left:0;">
                    <li>Hãng xe: {thuong_hieu}</li>
                    <li>Dòng xe: {dong_xe}</li>
                    <li>Loại xe: {loai_xe}</li>
                    <li>Xuất xứ: {nguon_goc}</li>
                </ul>
                <ul style="list-style-type:disc; padding-left:0;">
                    <li>Dung tích xi-lanh: {dung_tich_xi_lanh}</li>
                    <li>Năm đăng ký: {nam_dang_ky}</li>
                    <li>Số km đã đi: {so_km_da_di}</li>
                    <li>Khu vực của bạn: {quan}</li>
                </ul>
            </div>
            <hr style="border:1px solid #0ea5e9; margin:15px 0;">
            <h4 style="color:#0ea5e9;">💰 Giá dự đoán:</h4>
            <p style="color:#f472b6; font-size:1.3rem; font-weight:bold;">
                {formatted_price} VND
            </p>
        </div>

        """, unsafe_allow_html=True)
    



with tab4:
    iso_model = joblib.load("isolation_forest.joblib")
    rf_pipeline = joblib.load("residual_rf.joblib")
    with open("ensemble_weights.json","r") as f:
        weights = json.load(f)

    # Các hàm rule-based
    def business_rules(df):
        return ((df['price'] < 1) | (df['price'] > 500) | (df['km_driven'] > 200000)).astype(int)
    def modified_zscore(df, col='price'):
        median = df[col].median()
        mad = (df[col] - median).abs().median()
        z = 0.6745 * (df[col] - median) / mad
        return (abs(z) > 3.5).astype(int)
    def iqr_anomalies(df, col='price'):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        return ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).astype(int)
    def residual_anomalies(df, rf_pipeline, numeric_features, categorical_features, target):
        X = df[numeric_features + categorical_features]
        y_true = df[target]
        y_pred = rf_pipeline.predict(X)
        residuals = abs(y_true - y_pred)
        threshold = residuals.mean() + 2*residuals.std()
        return (residuals > threshold).astype(int)
    def ensemble(df, weights):
        score = (
            df['business']*weights['business'] +
            df['modified_z']*weights['modified_z'] +
            df['iqr']*weights['iqr'] +
            df['isolation']*weights['isolation'] +
            df['residual']*weights['residual']
        )
        return (score >= 0.5).astype(int), score

    # Streamlit UI
    st.markdown("""
    <h2 style="text-align:center; margin-bottom:10px;">
        Phát hiện bất thường
    </h2>
    <hr style="border:2px solid white; width:200px; margin:0 auto;margin-bottom:30px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color:#ffffff">
        Vui lòng nhập đầy đủ các thông tin bên dưới trước khi đăng bán sản phẩm.
    </p>

    """, unsafe_allow_html=True)

    # Form nhập tay
    col1, col2 = st.columns(2,gap="large")
    with col1:
        tab3_thuong_hieu = st.selectbox("Hãng xe", df['brand'].sort_values().unique(), key="tab3_brand")
        tab3_dong_xe = st.selectbox("Dòng xe", df['model'].sort_values().unique(),key="tab3_model")
        tab3_loai_xe = st.selectbox("Loại xe", df['vehicle_type'].sort_values().unique(),key="tab3_vehicle_type")
        tab3_nguon_goc = st.selectbox("Xuất xứ", df['origin'].sort_values().unique(),key="tab3_origin")

    with col2:
        tab3_dung_tich_xi_lanh = st.selectbox("Dung tích xi-lanh", df['engine_capacity'].sort_values().unique(),key="tab3_engine_capacity")
        tab3_nam_dang_ky = st.slider("Năm đăng ký", 1980, 2025, 2020,key="tab3_registration_year")
        tab3_so_km_da_di = st.number_input("Số km đã đi", min_value=0, max_value=200000, value=50000, step=1000,key="tab3_km_driven")
        tab3_quan = st.selectbox("Chọn quận của bạn", df['location'].sort_values().unique(),key="tab3_location")
        tab3_gia_dong= st.number_input("Giá bán", step=100_000,key="tab3_price_vnd")

    tab3_gia_trieu = tab3_gia_dong / 1_000_000

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    phat_hien_bat_thuong = st.button("Đăng bán")

    if phat_hien_bat_thuong:
        # Chuẩn bị dữ liệu đầu vào
        input_data = pd.DataFrame({
            "brand": [tab3_thuong_hieu],
            "model": [tab3_dong_xe],
            "vehicle_type": [tab3_loai_xe],
            "origin": [tab3_nguon_goc],
            "engine_capacity": [tab3_dung_tich_xi_lanh],
            "age": [2025 - tab3_nam_dang_ky],
            "km_driven": [tab3_so_km_da_di],
            "location": [tab3_quan],
            "price": [tab3_gia_trieu],
            "price_log": [np.log1p(tab3_gia_trieu)]
        })

        # Chạy anomaly detection cho input_data
        input_data['business'] = business_rules(input_data)
        input_data['modified_z'] = modified_zscore(input_data, 'price')
        input_data['iqr'] = iqr_anomalies(input_data, 'price')
        X_iso = input_data[['price','km_driven','age']].values
        input_data['isolation'] = (iso_model.predict(X_iso) == -1).astype(int)
        input_data['residual'] = residual_anomalies(input_data, rf_pipeline,
                                                    ['km_driven','age'],
                                                    ['brand','model','engine_capacity','vehicle_type','origin','location'],
                                                    'price_log')
        input_data['final_anomaly'], input_data['ensemble_score'] = ensemble(input_data, weights)
        result = input_data[['brand','model','price','km_driven','age','final_anomaly','ensemble_score']].copy()
        result['status'] = result['final_anomaly'].apply(lambda x: "Bình thường" if x == 0 else "Bất thường")       
        business_val   = int(input_data['business'].iloc[0])
        modified_val   = int(input_data['modified_z'].iloc[0])
        iqr_val        = int(input_data['iqr'].iloc[0])
        isolation_val  = int(input_data['isolation'].iloc[0])
        residual_val   = int(input_data['residual'].iloc[0])

        status = result['status'].iloc[0]
        if "Bình thường" in status:
            color = "white"
        else:
            color = "red"

        # Logic hiển thị chi tiết
        if status == "Bình thường":
            st.success("✅ Đăng bài thành công!")
        else:
            notes_text = (
                f"Business: {business_val}; "
                f"Modified Z-score: {modified_val}; "
                f"IQR: {iqr_val}; "
                f"Isolation Forest: {isolation_val}; "
                f"Residual: {residual_val}"
            )


            # Hiển thị trong cùng khung
            st.markdown(f"""
            <div style="
                border:2px solid #facc15;
                border-radius:8px;
                padding:15px;
                margin-top:15px;
                background-color:#1E293B;">
                <h4 style="color:#facc15;">⚠️ Cảnh báo bất thường:</h4>
                <p style="color:white; margin-top:10px;">
                    Mức giá bán hiện tại có sự chênh lệch khá lớn so với các sản phẩm tương tự trên thị trường.
                </p>
                <p style="color:white; margin-top:10px;">
                    Bạn có muốn tiếp tục đăng bài?
                    <span style="color:#22c55e; font-weight:bold;">Tiếp tục</span> /
                    <span style="color:#ef4444; font-weight:bold;">Hủy</span>
                </p>
            </div>
            """, unsafe_allow_html=True)


            new_id = 1
            timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            new_row = {
            "STT": new_id,
            "Thời gian": timestamp,
            "Hãng xe": tab3_thuong_hieu,
            "Dòng xe": tab3_dong_xe,
            "Loại xe": tab3_loai_xe,
            "Xuất xứ": tab3_nguon_goc,
            "Dung tích xi-lanh": tab3_dung_tich_xi_lanh,
            "Năm đăng ký": tab3_nam_dang_ky,
            "Số km đã đi": tab3_so_km_da_di,
            "Quận": tab3_quan,
            "Giá bán": tab3_gia_dong,
            "Tình trạng": status,
            "Ghi chú": notes_text if status == "Bất thường" else ""
            }
            df_display = pd.DataFrame([new_row])
            # Hiển thị bảng kết quả
            st.markdown("<div style='margin-top:60px'></div>", unsafe_allow_html=True)
            st.markdown("""
                <h2 style="text-align:center; margin-bottom:10px;">
                    Danh sách bài đăng bất thường
                </h2>
                <hr style="border:2px solid white; width:200px; margin:0 auto;margin-bottom:30px;">
            """, unsafe_allow_html=True)
            html_table = df_display.reset_index(drop=True)[[
                "STT","Thời gian","Hãng xe","Dòng xe","Loại xe","Xuất xứ",
                "Dung tích xi-lanh","Năm đăng ký","Số km đã đi","Quận",
                "Giá bán","Tình trạng","Ghi chú"
            ]].to_html(index=False)
            html_code = f"""
            <style>
            table.dataframe {{
                color: white;
                background-color: #1E293B;
                border-collapse: collapse;
                width: 100%;
            }}
            table.dataframe th {{
                color: white;
                background-color: #0ea5e9;
                padding: 8px;
            }}
            table.dataframe td {{
                color: white;
                padding: 8px;
            }}
            </style>
            {html_table}
            """

            components.html(html_code, height=400, scrolling=True)

 


# ===================  HẾT NỘI DUNG MENU ===================

# Done
     