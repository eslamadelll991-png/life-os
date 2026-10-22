import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="J.A.R.V.I.S | Life OS Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم واجهة فخمة ومريحة للعين (Dark Glassmorphism UI) داعمة للعربية بالكامل
st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    .pro-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 13px;
        color: #94a3b8;
        font-weight: 600;
    }
</style>
''', unsafe_allow_html=True)

# --- 2. إدارة الاتصال بـ Supabase ---
@st.cache_resource
def get_supabase():
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    if url and key:
        try:
            return create_client(url, key)
        except Exception as e:
            st.sidebar.error(f"خطأ ربط قاعدة البيانات: {e}")
            return None
    return None

supabase: Client = get_supabase()

# --- 3. الشريط الجانبي (Sidebar Navigation) ---
with st.sidebar:
    st.markdown("### ⚡ J.A.R.V.I.S OS")
    st.caption("نظام إدارة الإنتاجية والبيزنس المتكامل")
    
    if supabase:
        st.success("🟢 النظام متصل بالسحابة")
    else:
        st.warning("🟠 بانتظار تفعيل المفاتيح")
        
    st.markdown("---")
    menu = st.radio(
        "لوحات التحكم",
        [
            "⚡ المربع السحري (التفريغ والتدوين)",
            "💼 البيزنس والأرباح (المرحلة المربحة)",
            "🎯 العادات ونقاط الخبرة (Gamification)",
            "📊 مركز القيادة والتحليلات"
        ]
    )
    st.markdown("---")
    st.caption(f"التاريخ: {datetime.date.today().strftime('%Y-%m-%d')}")

# --- 4. الشاشة 1: المربع السحري الذكي ---
if menu == "⚡ المربع السحري (التفريغ والتدوين)":
    st.title("⚡ المربع السحري الذكي (Smart Brain Dump)")
    st.write("اكتب أفكارك، إنجازاتك، أو ملاحظاتك السريعة ليتم توثيقها وربطها تلقائياً بيومك.")
    
    col_input, col_stats = st.columns([2, 1])
    
    with col_input:
        with st.form("magic_box_form", clear_on_submit=True):
            user_text = st.text_area(
                "ماذا يدور في ذهنك أو ماذا أنجزت الآن؟",
                placeholder="مثال: خلصت اجتماع مهم، حققت مبيعة بقيمة 500 دولار، وجريت 3 كم...",
                height=150
            )
            c1, c2 = st.columns(2)
            with c1:
                category = st.selectbox("تصنيف الإدخال", ["بيزنس ومشاريع 💼", "تطوير ومهارات 💻", "صحة وعادات 🏃‍♂️", "تفريغ ذهني وأفكار 🧠", "روحانيات 🕊️"])
            with c2:
                energy_level = st.select_slider("مستوى طاقتك وتركيزك", options=["منخفض", "متوسط", "عالي", "Super Focus ⚡"], value="عالي")
                
            submit_log = st.form_submit_button("🚀 حفظ وتحليل الإدخال", use_container_width=True)
            
            if submit_log:
                if not user_text.strip():
                    st.warning("⚠️ الرجاء كتابة شيء أولاً.")
                else:
                    if supabase:
                        try:
                            record = {
                                "content": user_text,
                                "category": category,
                                "mood": energy_level,
                                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                            }
                            supabase.table("daily_logs").insert(record).execute()
                            st.success("✅ تم حفظ التدوينة بنجاح في قاعدة البيانات!")
                        except Exception as ex:
                            st.error(f"خطأ أثناء الحفظ: {ex}")
                    else:
                        st.info("💡 تم استلام النص بنجاح.")
    
    with col_stats:
        st.markdown('''
        <div class="pro-card">
            <div class="metric-label">تدوينات اليوم</div>
            <div class="metric-value">6 تدوينات</div>
        </div>
        <div class="pro-card">
            <div class="metric-label">سلسلة التدوين المتواصل</div>
            <div class="metric-value">🔥 14 يوماً</div>
        </div>
        ''', unsafe_allow_html=True)

# --- 5. الشاشة 2: البيزنس والأرباح (المرحلة المربحة) ---
elif menu == "💼 البيزنس والأرباح (المرحلة المربحة)":
    st.title("💼 إدارة البيزنس والتدفق المالي (Revenue Engine)")
    st.write("تتبع مبيعاتك، مصادر دخلك، ومصروفات المشاريع للوصول لأهدافك المالية الشهرية.")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="pro-card"><div class="metric-label">إجمالي دخل الشهر</div><div class="metric-value">4,250 $</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="pro-card"><div class="metric-label">المصروفات التشغيلية</div><div class="metric-value">620 $</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="pro-card"><div class="metric-label">صافي الربح المحقق</div><div class="metric-value">3,630 $</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="pro-card"><div class="metric-label">معدل تحقيق الهدف</div><div class="metric-value">72% 🎯</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    col_entry, col_history = st.columns([1, 1])
    with col_entry:
        st.subheader("➕ تسجيل معاملة مالية جديدة")
        with st.form("finance_form", clear_on_submit=True):
            amount = st.number_input("المبلغ ($)", min_value=1.0, step=10.0, value=100.0)
            trans_type = st.radio("نوع المعاملة", ["أرباح / دخل 💰", "مصروفات تشغيل 💳"], horizontal=True)
            source = st.text_input("المشروع / مصدر المعاملة", placeholder="مثال: استشارات تقنية، مبيعات منتج، اشتراكات...")
            submitted_finance = st.form_submit_button("تسجيل في الخزينة 💼", use_container_width=True)
            if submitted_finance:
                st.success(f"تم تسجيل {amount}$ في سجلات البيزنس بنجاح!")
                
    with col_history:
        st.subheader("📈 توزيع مصادر الدخل")
        income_sources = pd.DataFrame({
            "المصدر": ["الاستشارات البرمجية", "المشاريع الجانبية", "العمل الحر", "منتجات رقمية"],
            "القيمة ($)": [2100, 950, 750, 450]
        })
        st.bar_chart(income_sources.set_index("المصدر"))

# --- 6. الشاشة 3: العادات ونقاط الـ XP ---
elif menu == "🎯 العادات ونقاط الخبرة (Gamification)":
    st.title("🎯 نظام العادات وبناء الشخصية (Level Up)")
    st.write("حول حياتك إلى لعبة: كل عادة تنجزها تمنحك نقاط خبرة (XP) لترقية مستواك الشخصي.")
    
    st.markdown('''
    <div class="pro-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="metric-label">المستوى الحالي</div>
                <div class="metric-value">Level 9 — Master Builder ⚡</div>
            </div>
            <div style="text-align: left;">
                <div class="metric-label">نقاط الخبرة</div>
                <div style="font-size: 20px; font-weight: 700; color: #38bdf8;">8,450 / 10,000 XP</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.progress(0.84)
    
    st.markdown("---")
    st.subheader("✅ قائمة العادات اليومية")
    
    habits = [
        ("صلاة الفجر وقراءة ورد القرآن", "🕊️ روحانيات", 50),
        ("ساعتان تركيز عميق (Deep Work)", "💼 بيزنس وإنتاجية", 100),
        ("تمرين رياضي أو مشي 45 دقيقة", "🏃‍♂️ صحة وطاقة", 70),
        ("شرب 3 لتر ماء وتغذية نظيفة", "💧 صحة", 40),
        ("قراءة 15 صفحة من كتاب استراتيجي", "📚 تطوير ذات", 60),
    ]
    
    cols = st.columns(2)
    for idx, (habit_name, tag, xp) in enumerate(habits):
        with cols[idx % 2]:
            st.checkbox(f"{habit_name}  `+{xp} XP` ({tag})", key=f"habit_{idx}")

# --- 7. الشاشة 4: التحليلات والإحصائيات الشاملة ---
else:
    st.title("📊 مركز القيادة والتحليلات المتكاملة")
    st.write("نظرة شاملة من أعلى لرصد تطور جميع مسارات حياتك بصورة رقمية دقيقة.")
    
    weekly_perf = pd.DataFrame({
        "اليوم": ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"],
        "الإنتاجية": [85, 90, 95, 75, 88, 92, 80],
        "ساعات العمل العميق": [6, 7, 8, 5, 7.5, 8, 4]
    })
    
    st.subheader("📈 معدل الإنتاجية وساعات التركيز الأسبوعية")
    st.line_chart(weekly_perf.set_index("اليوم"))
    
    st.markdown("---")
    st.subheader("📜 أحدث التدوينات المسجلة على Supabase")
    if supabase:
        try:
            res = supabase.table("daily_logs").select("*").order("created_at", desc=True).limit(5).execute()
            if res.data:
                for item in res.data:
                    with st.expander(f"📌 {item.get('category', 'عام')} | {item.get('created_at', '')[:10]}"):
                        st.write(item.get("content", ""))
                        st.caption(f"الطاقة: {item.get('mood', 'جيد')}")
            else:
                st.info("لا توجد سجلات بعد في قاعدة البيانات. أضف أول تدوينة من المربع السحري.")
        except Exception:
            st.info("تأكد من وجود جدول `daily_logs` في قاعدة بيانات Supabase لعرض السجلات هنا.")
    else:
        st.info("ستظهر سجلاتك هنا فور إضافة بياناتك في قاعدة البيانات.")
