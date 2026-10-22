import streamlit as st
from supabase import create_client, Client
import datetime

# --- إعداد الصفحة العامة ---
st.set_page_config(
    page_title="Life OS | نظام إدارة الحياة",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- واجهة وتصميم مخصص ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .metric-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        color: #f8fafc;
        margin-bottom: 15px;
    }
    .metric-title { font-size: 14px; color: #94a3b8; margin-bottom: 6px; }
    .metric-val { font-size: 24px; font-weight: 700; color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# --- إعداد الاتصال بـ Supabase ---
def get_supabase_client():
    url = None
    key = None
    # محاولة القراءة من st.secrets أولاً
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    
    if url and key:
        try:
            return create_client(url, key)
        except Exception as e:
            st.sidebar.error(f"خطأ في الاتصال: {e}")
            return None
    return None

supabase: Client = get_supabase_client()

# --- القائمة الجانبية (Navigation) ---
with st.sidebar:
    st.markdown("### ⚡ Life OS")
    st.caption("نظام القيادة والإنتاجية الشخصية")
    st.markdown("---")
    menu = st.radio(
        "الانتقال السريع",
        ["📝 المربع السحري (التدوين)", "📊 لوحة المؤشرات", "⚙️ فحص الربط والإعدادات"]
    )
    st.markdown("---")
    if supabase:
        st.success("🟢 قاعدة البيانات متصلة")
    else:
        st.warning("🟠 بانتظار إدخال المفاتيح")

# --- 1. المربع السحري ---
if menu == "📝 المربع السحري (التدوين)":
    st.header("⚡ المربع السحري — التفريغ والتدوين اليومي")
    st.write("سجل كل ما يدور في ذهنك، مهامك، إنجازاتك أو ملاحظاتك في مساحة واحدة ليتم توثيقها تلقائياً.")

    with st.form("quick_log_form", clear_on_submit=True):
        entry_text = st.text_area(
            "ماذا تريد أن تسجل الآن؟",
            placeholder="مثال: أنجزت جلسة تركيز ساعتين على المشروع، شربت 2 لتر ماء، وقرأت 20 صفحة من الكتاب...",
            height=140
        )
        col1, col2 = st.columns(2)
        with col1:
            mood = st.select_slider("المزاج / مستوى الطاقة", options=["منخفض جداً", "منخفض", "متوسط", "جيد", "ممتاز"], value="جيد")
        with col2:
            tag = st.selectbox("تصنيف التدوينة", ["إنجاز عمل", "صحة وعادات", "تطوير ذاتي", "مصروفات وماليات", "أفكار عابرة"])

        submitted = st.form_submit_button("💾 حفظ في قاعدة البيانات", use_container_width=True)

        if submitted:
            if not entry_text.strip():
                st.warning("⚠️ يُرجى كتابة نص التدوينة أولاً.")
            elif not supabase:
                st.error("⚠️ لم يتم ربط Supabase بعد. انتقل لصفحة 'فحص الربط والإعدادات' لإضافة المفاتيح.")
            else:
                try:
                    payload = {
                        "content": entry_text,
                        "mood": mood,
                        "category": tag,
                        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                    }
                    supabase.table("daily_logs").insert(payload).execute()
                    st.success("✅ تم حفظ التدوينة في قاعدة البيانات بنجاح!")
                except Exception as ex:
                    st.error(f"حدث خطأ أثناء الحفظ: {ex}")

# --- 2. لوحة المؤشرات ---
elif menu == "📊 لوحة المؤشرات":
    st.header("📊 ملخص الأداء ومتابعة الحياة")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('''
        <div class="metric-box">
            <div class="metric-title">مؤشر التركيز الأسبوعي</div>
            <div class="metric-val">88%</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
        <div class="metric-box">
            <div class="metric-title">سلسلة الالتزام (Streak)</div>
            <div class="metric-val">12 يوماً 🔥</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown('''
        <div class="metric-box">
            <div class="metric-title">حالة النظام</div>
            <div class="metric-val">مستقر 100%</div>
        </div>
        ''', unsafe_allow_html=True)

    st.subheader("سجل التدوينات الأخيرة")
    if supabase:
        try:
            data = supabase.table("daily_logs").select("*").order("created_at", desc=True).limit(5).execute()
            if data.data:
                for row in data.data:
                    with st.expander(f"📌 {row.get('category', 'عام')} — {row.get('created_at', '')[:10]}"):
                        st.write(row.get('content', ''))
                        st.caption(f"المزاج: {row.get('mood', 'غير محدد')}")
            else:
                st.info("لا توجد تدوينات مسجلة بعد. ابدأ بإضافة أول تدوينة من المربع السحري.")
        except Exception:
            st.info("لم نتمكن من جلب السجلات. تأكد من وجود جدول `daily_logs` في قاعدة بياناتك.")
    else:
        st.info("ستظهر سجلاتك هنا فور إتمام ربط قاعدة البيانات.")

# --- 3. فحص الربط والإعدادات ---
else:
    st.header("⚙️ إعدادات النظام وربط Supabase")
    st.write("لربط التطبيق بقاعدة بياناتك على السيرفر السحابي، اتبع الخطوات التالية:")

    st.markdown("""
    ### أين تضع المفاتيح في Streamlit Cloud؟
    1. في صفحة تطبيقك على **Streamlit Cloud**، اضغط على النقاط الثلاث **(...)** بجانب التطبيق ثم اختر **Settings**.
    2. اختر تبويب **Secrets**.
    3. الصق المتغيرات بالشكل التالي تماماً:
    """)

    st.code("""
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
    """, language="toml")

    if supabase:
        st.success("🎉 التطبيق متصل ومستعد لحفظ واسترجاع بياناتك بكل أمان!")
    else:
        st.warning("⚠️ بانتظار إدخال المفاتيح في إعدادات المنصة.")
