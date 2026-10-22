import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="J.A.R.V.I.S Life OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم وتنسيق CSS احترافي للواجهة
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1e293b;
        color: white;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# الاتصال بقاعدة بيانات Supabase باستخدام متغيرات البيئة أو السكرت
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        # قيم افتراضية للاختبار لو لم تُضبط الأسرار بعد
        return None

supabase = init_supabase()

# الشريط الجانبي
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("J.A.R.V.I.S OS")
    st.markdown("---")
    app_mode = st.radio("القائمة الرئيسية", ["🚀 المربع السحري واليوميات", "📊 لوحة المؤشرات والعادات", "⚙️ الإعدادات وحالة النظام"])
    st.markdown("---")
    st.caption("© 2026 Life OS - جميع الحقوق محفوظة")

# الصفحة الأولى: المربع السحري الذكي
if app_mode == "🚀 المربع السحري واليوميات":
    st.title("⚡ المربع السحري الذكي")
    st.markdown("سجل تفاصيل يومك، إنجازاتك، مصروفاتك، أو أفكارك في جملة واحدة، وسيقوم النظام بتحليلها وحفظها مباشرة.")
    
    with st.form("magic_form", clear_on_submit=True):
        user_input = st.text_area("ماذا انجزت اليوم أو ما هي تفاصيل يومك؟", placeholder="مثال: ذاكرت 3 ساعات برمجة بايثون، وصرفت 150 جنيه أكل، وصليت الصلوات في وقتها...", height=120)
        mood = st.slider("مستوى طاقتك المزاجية اليوم (من 1 إلى 10):", 1, 10, 8)
        submitted = st.form_submit_button("تحليل وحفظ في قاعدة البيانات 🚀")
        
        if submitted:
            if user_input.strip():
                if supabase:
                    try:
                        # إرسال البيانات لجدول mental_daily_logs في Supabase
                        data = {
                            "morning_10_lines": user_input,
                            "mood_score": mood
                        }
                        res = supabase.table("mental_daily_logs").insert(data).execute()
                        st.success("✨ تم حفظ البيانات وتحليلها في قاعدة البيانات بنجاح!")
                    except Exception as ex:
                        st.error(فشل الاتصال بقاعدة البيانات أو حفظ البيانات: {ex})
                else:
                    st.warning("⚠️ تم استقبال النص بنجاح، لكن يرجى ضبط مفاتيح Supabase في إعدادات المنصة.")
                    st.info(f"النص المدخل: {user_input}")
            else:
                st.warning("الرجاء إدخال نص أولاً.")

# الصفحة الثانية: المؤشرات
elif app_mode == "📊 لوحة المؤشرات والعادات":
    st.title("📊 لوحة القيادة والمؤشرات")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>طاقة اليوم</h3><h2>⚡ 90%</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>الخبرة (XP)</h3><h2>⭐ Level 12</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>المهام المنجزة</h3><h2>✅ 8/10</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>المصروفات</h3><h2>💸 240 EGP</h2></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📈 تتبع النشاط الأسبوعي")
    chart_data = pd.DataFrame({
        'الأيام': ['السبت', 'الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
        'الإنتاجية': [80, 85, 90, 70, 95, 88, 92]
    })
    st.line_chart(chart_data.set_index('الأيام'))

# الصفحة الثالثة: الإعدادات
else:
    st.title("⚙️ إعدادات النظام وحالة الاتصال")
    st.markdown("تحقق من ربط قاعدة البيانات ومنصة الاستضافة.")
    if supabase:
        st.success("🟢 متصل بقاعدة بيانات Supabase بنجاح!")
    else:
        st.warning("🟡 لم يتم العثور على مفاتيح Supabase في الـ Secrets.")
    
    st.markdown("### 🔑 إرشادات ربط المفاتيح:")
    st.code("SUPABASE_URL = 'رابط_المشروع_هنا'\nSUPABASE_KEY = 'المفتاح_السري_هنا'")
