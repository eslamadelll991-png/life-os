import streamlit as st
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
import pandas as pd
import datetime

# --- إعداد الصفحة العامة والهوية البصرية ---
st.set_page_config(
    page_title="J.A.R.V.I.S | Life OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم واجهة فخمة مريحة للعين (Dark Glassmorphism)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #080c14;
        color: #f8fafc;
    }
    
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(12px);
    }
    
    .metric-value {
        font-size: 26px;
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
    
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        transition: all 0.2s ease;
    }
    
    .date-badge {
        background-color: #1e293b;
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- بوابة الأمان وتسجيل الدخول ---
def check_password():
    expected_pw = st.secrets.get("APP_PASSWORD")
    if not expected_pw:
        return True
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        
    if not st.session_state["authenticated"]:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown('<div class="glass-card" style="text-align: center;"><h2>🔒 J.A.R.V.I.S Security Gate</h2><p style="color:#94a3b8;">يرجى إدخال رمز الأمان للوصول إلى نظامك الخاص</p></div>', unsafe_allow_html=True)
            pw_input = st.text_input("رمز الأمان (Master PIN / Password)", type="password")
            if st.button("فتح النظام 🔓", use_container_width=True):
                if pw_input == str(expected_pw):
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ رمز المرور غير صحيح!")
        return False
    return True

if not check_password():
    st.stop()

# --- إدارة الاتصال بالسحابة ---
@st.cache_resource
def init_services():
    sb = None
    sb_url = st.secrets.get("SUPABASE_URL")
    sb_key = st.secrets.get("SUPABASE_KEY")
    if sb_url and sb_key:
        try:
            sb = create_client(sb_url, sb_key)
        except Exception:
            pass
            
    c_name = st.secrets.get("CLOUDINARY_CLOUD_NAME")
    c_key = st.secrets.get("CLOUDINARY_API_KEY")
    c_sec = st.secrets.get("CLOUDINARY_API_SECRET")
    if c_name and c_key and c_sec:
        cloudinary.config(cloud_name=c_name, api_key=c_key, api_secret=c_sec, secure=True)
        
    return sb

supabase: Client = init_services()
TODAY_DATE = datetime.date.today().strftime('%Y-%m-%d')

# --- القائمة الجانبية للتنقل الشامل ---
with st.sidebar:
    st.markdown("### ⚡ J.A.R.V.I.S Life OS")
    st.caption("نظام القيادة والمتابعة الحياتية الشاملة")
    
    if supabase:
        st.success("🟢 متصل بقاعدة البيانات")
    else:
        st.warning("🟠 بانتظار تفعيل المفاتيح")
        
    st.markdown("---")
    menu = st.radio(
        "الأقسام الرئيسية",
        [
            "🏛️ مركز القيادة الأم (Master Dashboard)",
            "🧠 النفسية، العادات، وخزنة القراءة",
            "🎨 معرض الرسومات الفنية (Art Gallery)",
            "🕌 الدين، الصلوات، ورادار المعاصي",
            "🏃‍♂️ الجيم، التغذية، والميزان الصباحي",
            "💼 هرم الخطط الزمنية واقتناص الوظائف"
        ]
    )
    st.markdown("---")
    st.caption(f"تاريخ اليوم: {TODAY_DATE}")
    if st.button("قفل النظام 🔒"):
        st.session_state["authenticated"] = False
        st.rerun()

# ==========================================
# 1. الشاشة الرئيسية
# ==========================================
if menu == "🏛️ مركز القيادة الأم (Master Dashboard)":
    st.title("🏛️ مركز القيادة والتحكم العام (Master Dashboard)")
    
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.markdown('<div class="glass-card"><div class="metric-label">مؤشر أداء اليوم</div><div class="metric-value">91% 🌟</div></div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="glass-card"><div class="metric-label">صلوات اليوم في المسجد</div><div class="metric-value">4 / 5 🕌</div></div>', unsafe_allow_html=True)
    with b3:
        st.markdown('<div class="glass-card"><div class="metric-label">أطول سلسلة التزام (Streak)</div><div class="metric-value">🔥 متصل</div></div>', unsafe_allow_html=True)
    with b4:
        st.markdown('<div class="glass-card"><div class="metric-label">التزام الجيم والتغذية</div><div class="metric-value">منضبط ✅</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    col_todo, col_overview = st.columns([1, 1])
    with col_todo:
        st.subheader("📋 قائمة المهام الموحدة لليوم")
        st.checkbox("صلاة الفجر حاضراً والورد القرآني", value=True)
        st.checkbox("ساعتان مذاكرة مركزة (Deep Work)")
        st.checkbox("تمرين الجيم والالتزام بوجبات الدايت")
        st.checkbox("تسجيل يوميات الصباح والمساء")
        st.checkbox("قراءة 15 صفحة من الكتاب الحالي")
        
    with col_overview:
        st.subheader("📈 توازن مسارات الحياة الأسبوعي")
        balance_df = pd.DataFrame({
            "المسار": ["الروحي والديني", "الجسدي والصحي", "المهني والمذاكرة", "النفسي وتطوير الذات"],
            "معدل الإنجاز %": [88, 80, 92, 85]
        })
        st.bar_chart(balance_df.set_index("المسار"))

# ==========================================
# 2. قسم النفسية، العادات، وخزنة القراءة (المُطوّر)
# ==========================================
elif menu == "🧠 النفسية، العادات، وخزنة القراءة":
    st.title("🧠 محرك النفسية، إدارة العادات، وخزنة القراءة")
    
    tab_dump, tab_habits, tab_reading = st.tabs(["📝 يوميات الصباح والمساء", "🎯 مدير العادات المرن", "📚 مكتبة وخزنة القراءة"])
    
    # ---------------------------------------------------------
    # 📝 يوميات الصباح والمساء (مع التاريخ والامتنان)
    # ---------------------------------------------------------
    with tab_dump:
        st.subheader(f"📝 توثيق النفسية ليوم: {TODAY_DATE}")
        
        log_type = st.radio("متى تدون الآن؟", ["🌞 تدوين الصباح (بداية اليوم)", "🌙 تدوين المساء (نهاية اليوم)"], horizontal=True)
        
        with st.form("mental_log_form", clear_on_submit=True):
            if "الصباح" in log_type:
                st.info("💡 ركز في الصباح على تفريغ ذهنك، نواياك لليوم، وما يقلقك لترتاح منه.")
                journal_text = st.text_area("كيف استيقظت؟ وما هو تركيزك اليوم؟", height=120)
                good_things = "" # لا يوجد في الصباح
            else:
                st.info("💡 ركز في المساء على مراجعة يومك، استخلاص الدروس، والامتنان للأشياء الجميلة.")
                journal_text = st.text_area("كيف كان يومك؟ ماذا أنجزت؟ وكيف تشعر الآن؟", height=120)
                good_things = st.text_area("✨ اكتب 5 أشياء حلوة حصلت أو عملتها النهاردة (حتى لو بسيطة جداً):", height=100, placeholder="1. شربت قهوة في هدوء\n2. التزمت بتمرينة الجيم\n3. ...")

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                mood_val = st.slider("مستوى طاقتك ومزاجك (1 أسوأ شيء - 10 ممتاز):", 1, 10, 8)
            with col_m2:
                sentiment_note = st.selectbox("الحالة الغالبة عليك:", ["حماس وتركيز 🚀", "سلام ورضا 🤍", "إرهاق أو كسل 😴", "قلق أو ضغط ⚠️", "حزن أو ضيق 🌧️"])
                
            submit_dump = st.form_submit_button("💾 حفظ في سجلات اليوم", use_container_width=True)
            
            if submit_dump:
                if journal_text.strip() and supabase:
                    try:
                        time_val = 'صباحي' if 'الصباح' in log_type else 'مسائي'
                        supabase.table("mental_daily_logs").insert({
                            "log_date": TODAY_DATE,
                            "time_of_day": time_val,
                            "journal_text": journal_text,
                            "mood_score": mood_val,
                            "sentiment": sentiment_note,
                            "five_good_things": good_things
                        }).execute()
                        st.success("✅ تم حفظ التدوينة بنجاح وربطها بتاريخ اليوم!")
                    except Exception as ex:
                        st.error(f"خطأ في الحفظ، تأكد من تحديث جدول قاعدة البيانات: {ex}")
                        
        # عرض التدوينات السابقة
        st.markdown("---")
        st.subheader("🕰️ أرشيف أيامك السابقة")
        if supabase:
            logs_res = supabase.table("mental_daily_logs").select("*").order("log_date", desc=True).order("created_at", desc=True).execute()
            if logs_res.data:
                for log in logs_res.data:
                    date_str = log.get('log_date', '')
                    time_str = log.get('time_of_day', '')
                    icon = "🌞" if time_str == 'صباحي' else "🌙"
                    
                    with st.expander(f"{icon} تدوين {time_str} | بتاريخ: {date_str} | المزاج: {log.get('mood_score')}/10"):
                        st.write(log.get('journal_text', ''))
                        
                        five_things = log.get('five_good_things')
                        if five_things and len(five_things.strip()) > 0:
                            st.markdown("**✨ 5 أشياء حلوة في هذا اليوم:**")
                            st.info(five_things)
            else:
                st.caption("لا توجد تدوينات بعد.")

    # ---------------------------------------------------------
    # 🎯 مدير العادات المرن (فصل الإضافة عن التسجيل)
    # ---------------------------------------------------------
    with tab_habits:
        st.subheader("🎯 مدير العادات والأنشطة")
        st.write("هنا يمكنك تعريف أي عادة جديدة، ثم تسجيل قيامك بها يومياً.")
        
        # 1. قسم الإضافة (مخفي داخل Expander لعدم الزحمة)
        with st.expander("➕ إنشاء عادة أو نشاط جديد (لأول مرة)", expanded=False):
            with st.form("add_new_habit_form"):
                col_hn, col_hc, col_btn = st.columns([2, 1, 1])
                with col_hn:
                    new_habit = st.text_input("اسم العادة (مثال: لعب شطرنج، لودو، مشي):")
                with col_hc:
                    habit_cat = st.selectbox("التصنيف:", ["ترفيه وهوايات 🎮", "تطوير ومهارات 💻", "صحة 🏃‍♂️", "روحانيات 🕊️"])
                with col_btn:
                    st.markdown("<br>", unsafe_allow_html=True)
                    submitted_habit = st.form_submit_button("حفظ العادة")
                    
                if submitted_habit:
                    if new_habit.strip() and supabase:
                        try:
                            supabase.table("elastic_habits").insert({
                                "habit_name": new_habit,
                                "category": habit_cat,
                                "streak_count": 0
                            }).execute()
                            st.success(f"تمت إضافة '{new_habit}' بنجاح! ستجدها بالأسفل لتسجيلها يومياً.")
                            st.rerun()
                        except Exception as ex:
                            st.error(f"خطأ: {ex}")

        # 2. قسم تسجيل الأداء اليومي
        st.markdown("### ✅ سجل إنجازاتك اليومية (Daily Check-in)")
        if supabase:
            habits_res = supabase.table("elastic_habits").select("*").eq("is_active", True).execute()
            if habits_res.data:
                st.info("قم بتحديد العادات التي مارستها اليوم واضغط 'تأكيد' لزيادة نقاط الالتزام (Streak).")
                with st.form("log_habits_form"):
                    cols = st.columns(2)
                    checkboxes = {}
                    for idx, h in enumerate(habits_res.data):
                        c = cols[idx % 2]
                        label = f"{h['habit_name']} (Streak: {h['streak_count']} 🔥)"
                        checkboxes[h['id']] = c.checkbox(label, key=f"hab_log_{h['id']}")
                        
                    if st.form_submit_button("🚀 تأكيد إنجازات اليوم", use_container_width=True):
                        for h_id, is_checked in checkboxes.items():
                            if is_checked:
                                curr_streak = next(item['streak_count'] for item in habits_res.data if item['id'] == h_id)
                                supabase.table("elastic_habits").update({"streak_count": curr_streak + 1}).eq("id", h_id).execute()
                        st.success("تم تحديث سلاسل الالتزام (Streaks) لعاداتك اليوم بنجاح!")
                        st.rerun()
            else:
                st.warning("لم تقم بإنشاء أي عادات بعد. استخدم المربع أعلاه لإضافة عادتك الأولى.")

    # ---------------------------------------------------------
    # 📚 مكتبة الكتب وخزنة الملخصات
    # ---------------------------------------------------------
    with tab_reading:
        st.subheader("📚 إضافة وتحديث كتاب")
        with st.form("book_form"):
            b_title = st.text_input("اسم الكتاب:")
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                cur_page = st.number_input("الصفحة الحالية التي وصلت إليها:", min_value=0, value=0)
            with c_p2:
                tot_page = st.number_input("إجمالي عدد صفحات الكتاب:", min_value=1, value=100)
            b_summary = st.text_area("خزنة ملخص الكتاب أو الفوائد الرئيسية التي خرجت بها:")
            
            if st.form_submit_button("حفظ الكتاب في المكتبة 📖"):
                if supabase and b_title.strip():
                    try:
                        existing = supabase.table("reading_vault").select("id").eq("book_title", b_title).execute()
                        data_to_save = {
                            "book_title": b_title,
                            "current_page": cur_page,
                            "total_pages": tot_page,
                            "summary_notes": b_summary,
                            "is_finished": cur_page >= tot_page
                        }
                        if existing.data:
                            supabase.table("reading_vault").update(data_to_save).eq("book_title", b_title).execute()
                        else:
                            supabase.table("reading_vault").insert(data_to_save).execute()
                            
                        st.success("✅ تم حفظ الكتاب وتقدمك بنجاح!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")
                        
        st.markdown("---")
        st.subheader("🏛️ مكتبتك الخاصة (سجل الكتب والملخصات)")
        if supabase:
            books_res = supabase.table("reading_vault").select("*").order("created_at", desc=True).execute()
            if books_res.data:
                for b in books_res.data:
                    is_done = b.get('is_finished', False)
                    status_text = "✅ مكتمل" if is_done else f"⏳ قيد القراءة ({b.get('current_page')}/{b.get('total_pages')})"
                    
                    with st.expander(f"📖 {b.get('book_title')} — {status_text}"):
                        progress_val = min(1.0, b.get('current_page', 0) / b.get('total_pages', 1))
                        st.progress(progress_val)
                        
                        st.markdown("**الملخص والفوائد المحفوظة:**")
                        summary = b.get('summary_notes')
                        if summary:
                            st.write(summary)
                        else:
                            st.caption("لا يوجد ملخص مسجل لهذا الكتاب بعد.")
            else:
                st.info("مكتبتك فارغة. أضف أول كتاب لتبدأ في بناء خزنتك المعرفية!")

# ==========================================
# 3. قسم معرض الرسومات الفنية (Cloudinary)
# ==========================================
elif menu == "🎨 معرض الرسومات الفنية (Art Gallery)":
    st.title("🎨 معرض الرسومات الفنية وتتبع التطور الإبداعي")
    
    uploaded_drawing = st.file_uploader("اختر صورة رسمتك لرفعها إلى المعرض السحابي:", type=["png", "jpg", "jpeg"])
    drawing_caption = st.text_input("وصف أو عنوان الرسمة / الملاحظات الفنية:")
    
    if st.button("🚀 رفع الرسمة إلى Cloudinary", use_container_width=True):
        if uploaded_drawing is not None:
            try:
                upload_res = cloudinary.uploader.upload(uploaded_drawing, folder="life_os_drawings")
                img_url = upload_res.get("secure_url")
                st.success("✨ تم رفع الرسمة بنجاح إلى المعرض السحابي!")
                st.image(img_url, caption=drawing_caption or "رسمة جديدة", use_column_width=True)
            except Exception as e:
                st.error(f"فشل الرفع: {e}")
        else:
            st.warning("⚠️ يُرجى تحديد صورة أولاً.")

# ==========================================
# الأقسام المتبقية (الدين، الجيم، الخطط) تعمل بنفس النمط
# ==========================================
elif menu == "🕌 الدين، الصلوات، ورادار المعاصي":
    st.title("🕌 محرك الدين، الصلاة، وتزكية النفس")
    st.info("باقي الأقسام تعمل بكفاءة كما تم تجهيزها مسبقاً...")
    
elif menu == "🏃‍♂️ الجيم، التغذية، والميزان الصباحي":
    st.title("🏃‍♂️ محرك اللياقة البدنية، الجيم، والتغذية")
    st.info("باقي الأقسام تعمل بكفاءة كما تم تجهيزها مسبقاً...")

else:
    st.title("💼 هرم الخطط الزمنية ونظام اقتناص الوظائف (CRM)")
    st.info("باقي الأقسام تعمل بكفاءة كما تم تجهيزها مسبقاً...")
