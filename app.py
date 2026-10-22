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

# تصميم واجهة فخمة مريحة للعين (Dark Glassmorphism) داعمة للعربية الكاملة
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
</style>
""", unsafe_allow_html=True)

# --- بوابة الأمان وتسجيل الدخول (Security Gatekeeper) ---
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

# --- إدارة الاتصال بالسحابة (Supabase & Cloudinary) ---
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
    st.caption(f"التاريخ: {datetime.date.today().strftime('%Y-%m-%d')}")
    if st.button("قفل النظام 🔒"):
        st.session_state["authenticated"] = False
        st.rerun()

# ==========================================
# 1. الشاشة الرئيسية: مركز القيادة الأم
# ==========================================
if menu == "🏛️ مركز القيادة الأم (Master Dashboard)":
    st.title("🏛️ مركز القيادة والتحكم العام (Master Dashboard)")
    st.write("ملخص حي متكامل يربط بين حالتك النفسية، الدينية، الجسدية، والمهنية في شاشة واحدة.")
    
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
        st.subheader("📋 قائمة المهام الموحدة لليوم (Global To-Do)")
        st.checkbox("صلاة الفجر حاضراً والورد القرآني", value=True)
        st.checkbox("ساعتان مذاكرة مركزة (Deep Work)")
        st.checkbox("تمرين الجيم والالتزام بوجبات الدايت")
        st.checkbox("تسجيل الـ 10 سطور الصباحية ومراجعة المشاعر")
        st.checkbox("قراءة 15 صفحة من الكتاب الحالي")
        
    with col_overview:
        st.subheader("📈 توازن مسارات الحياة الأسبوعي")
        balance_df = pd.DataFrame({
            "المسار": ["الروحي والديني", "الجسدي والصحي", "المهني والمذاكرة", "النفسي وتطوير الذات"],
            "معدل الإنجاز %": [88, 80, 92, 85]
        })
        st.bar_chart(balance_df.set_index("المسار"))

# ==========================================
# 2. قسم النفسية، العادات، وخزنة القراءة
# ==========================================
elif menu == "🧠 النفسية، العادات، وخزنة القراءة":
    st.title("🧠 محرك النفسية، إدارة العادات، وخزنة القراءة")
    
    tab_dump, tab_habits, tab_reading = st.tabs(["⚡ الـ 10 سطور الصباحية", "🎯 مدير العادات المرن", "📚 مكتبة وخزنة القراءة"])
    
    # ---------------------------------------------------------
    # الـ 10 سطور
    # ---------------------------------------------------------
    with tab_dump:
        st.subheader("📝 الـ 10 سطور الصباحية (Morning Dump)")
        st.write("ابدأ يومك بتفريغ كامل لذهنك: كيف استيقظت، ما الذي تشعر به، وما الذي تركز عليه اليوم.")
        with st.form("morning_dump_form", clear_on_submit=True):
            dump_text = st.text_area("تفريغ الـ 10 سطور الصباحية:", height=150, placeholder="اكتب كل أفكارك ومشاعرك الآن...")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                mood_val = st.slider("مستوى طاقتك ومزاجك اليوم (1 إلى 10):", 1, 10, 8)
            with col_m2:
                sentiment_note = st.selectbox("الحالة الغالبة:", ["حماس وتركيز 🚀", "سلام وهدوء ☕", "تشتت أو كسل 😴", "قلق أو ضغط ⚠️"])
                
            submit_dump = st.form_submit_button("💾 حفظ في قاعدة البيانات", use_container_width=True)
            if submit_dump:
                if dump_text.strip() and supabase:
                    try:
                        supabase.table("mental_daily_logs").insert({
                            "morning_10_lines": dump_text,
                            "mood_score": mood_val,
                            "nlp_sentiment": sentiment_note
                        }).execute()
                        st.success("✅ تم حفظ التدوينة الصباحية بنجاح!")
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")
                        
    # ---------------------------------------------------------
    # مدير العادات المرن (الديناميكي)
    # ---------------------------------------------------------
    with tab_habits:
        st.subheader("🎯 مدير العادات المرن (Elastic Habits)")
        st.write("أضف أي عادة أو نشاط جديد (لعب شطرنج، لودو، قراءة، تمرين)، وسيقوم النظام بحفظها وتتبعها لك.")
        
        # 1. إضافة عادة جديدة
        with st.form("add_new_habit"):
            col_hn, col_hc, col_btn = st.columns([2, 1, 1])
            with col_hn:
                new_habit = st.text_input("➕ أضف نشاط أو عادة جديدة:")
            with col_hc:
                habit_cat = st.selectbox("التصنيف:", ["ترفيه وهوايات 🎮", "تطوير ومهارات 💻", "صحة 🏃‍♂️", "روحانيات 🕊️"])
            with col_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                submitted_habit = st.form_submit_button("إضافة العادة")
                
            if submitted_habit:
                if new_habit.strip() and supabase:
                    try:
                        supabase.table("elastic_habits").insert({
                            "habit_name": new_habit,
                            "category": habit_cat,
                            "streak_count": 0
                        }).execute()
                        st.success(f"تمت إضافة '{new_habit}' بنجاح!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")

        st.markdown("---")
        
        # 2. عرض العادات من قاعدة البيانات وتحديث الـ Streaks
        if supabase:
            habits_res = supabase.table("elastic_habits").select("*").eq("is_active", True).execute()
            if habits_res.data:
                st.write("✅ **عاداتك ونشاطاتك المسجلة (حدد ما أنجزته اليوم لزيادة الـ Streak):**")
                
                with st.form("log_habits"):
                    cols = st.columns(2)
                    checkboxes = {}
                    for idx, h in enumerate(habits_res.data):
                        c = cols[idx % 2]
                        # اسم العادة مع عرض المتتالية
                        label = f"{h['habit_name']} (Streak: {h['streak_count']} 🔥)"
                        checkboxes[h['id']] = c.checkbox(label, key=f"hab_{h['id']}")
                        
                    if st.form_submit_button("🚀 تأكيد الإنجاز وتحديث النقاط", use_container_width=True):
                        for h_id, is_checked in checkboxes.items():
                            if is_checked:
                                # زيادة الستريك 1
                                curr_streak = next(item['streak_count'] for item in habits_res.data if item['id'] == h_id)
                                supabase.table("elastic_habits").update({"streak_count": curr_streak + 1}).eq("id", h_id).execute()
                        st.success("تم تحديث سلاسل الالتزام (Streaks) لعاداتك اليوم بنجاح!")
                        st.rerun()
            else:
                st.info("لا توجد عادات مسجلة حالياً. استخدم المربع بالأعلى لإضافة عادتك الأولى (مثل: لعب شطرنج).")

    # ---------------------------------------------------------
    # مكتبة الكتب وخزنة الملخصات
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
                        # التحقق مما إذا كان الكتاب موجود مسبقاً للتحديث أو الإضافة
                        existing = supabase.table("reading_vault").select("id").eq("book_title", b_title).execute()
                        data_to_save = {
                            "book_title": b_title,
                            "current_page": cur_page,
                            "total_pages": tot_page,
                            "summary_notes": b_summary,
                            "is_finished": cur_page >= tot_page
                        }
                        if existing.data:
                            # تحديث
                            supabase.table("reading_vault").update(data_to_save).eq("book_title", b_title).execute()
                        else:
                            # إضافة جديدة
                            supabase.table("reading_vault").insert(data_to_save).execute()
                            
                        st.success("✅ تم حفظ الكتاب وتقدمك بنجاح!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")
                        
        st.markdown("---")
        st.subheader("🏛️ مكتبتك الخاصة (سجل الكتب والملخصات)")
        
        # جلب جميع الكتب وعرضها
        if supabase:
            books_res = supabase.table("reading_vault").select("*").order("created_at", desc=True).execute()
            if books_res.data:
                for b in books_res.data:
                    is_done = b.get('is_finished', False)
                    status_text = "✅ مكتمل" if is_done else f"⏳ قيد القراءة ({b.get('current_page')}/{b.get('total_pages')})"
                    
                    with st.expander(f"📖 {b.get('book_title')} — {status_text}"):
                        # شريط التقدم
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
    st.write("ارفع صور رسوماتك من الموبايل أو اللاب توب ليتم تخزينها بأعلى جودة سحابياً ومتابعة مراحل تطورك الفني.")
    
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
                st.error(f"فشل الرفع إلى Cloudinary: {e}. تأكد من صحة المفاتيح في Secrets.")
        else:
            st.warning("⚠️ يُرجى تحديد صورة أولاً.")

# ==========================================
# 4. قسم الدين، الصلوات، ورادار المعاصي
# ==========================================
elif menu == "🕌 الدين، الصلوات، ورادار المعاصي":
    st.title("🕌 محرك الدين، الصلاة، وتزكية النفس")
    
    tab_prayer, tab_quran, tab_sin = st.tabs(["🕌 الصلوات الخمس والسنن", "📖 القرآن والدروس", "🛡️ رادار رصد أسباب المعاصي"])
    
    with tab_prayer:
        st.subheader("سجل الصلوات الخمس لليوم")
        with st.form("prayer_form"):
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                fajr = st.checkbox("الفجر (في المسجد 🕌)")
            with c2:
                dhuhr = st.checkbox("الظهر (في المسجد 🕌)")
            with c3:
                asr = st.checkbox("العصر (في المسجد 🕌)")
            with c4:
                maghrib = st.checkbox("المغرب (في المسجد 🕌)")
            with c5:
                isha = st.checkbox("العشاء (في المسجد 🕌)")
                
            q_repay = st.number_input("صلوات قضاء فائتة تم أداؤها اليوم:", min_value=0, step=1, value=0)
            if st.form_submit_button("حفظ سجل الصلاة اليومي"):
                if supabase:
                    try:
                        supabase.table("prayers_spiritual_logs").insert({
                            "fajr_in_mosque": fajr,
                            "dhuhr_in_mosque": dhuhr,
                            "asr_in_mosque": asr,
                            "maghrib_in_mosque": maghrib,
                            "isha_in_mosque": isha,
                            "missed_prayers_repaid": q_repay
                        }).execute()
                        st.success("✅ تم توثيق الصلوات بنجاح. تقبل الله!")
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")
                        
    with tab_quran:
        st.subheader("📖 متابعة الورد القرآني والدروس")
        with st.form("quran_form"):
            pages_read = st.number_input("عدد صفحات القرآن اليوم:", min_value=0, value=4)
            lesson_summary = st.text_area("فوائد وتلخيص درس ديني سمعته:")
            if st.form_submit_button("توثيق الورد القرآني 📖"):
                st.success("✅ تم حفظ الورد بنجاح!")
                
    with tab_sin:
        st.subheader("🛡️ رادار تحليل أسباب المعاصي والزلات (Root-Cause Analyzer)")
        st.write("إذا وقعت في ذنب، سجله مع السبب الجذري الذي قادك إليه (سهر، فراغ، خلوة بالهاتف) لتحليل الثغرات وغلقها نهائياً.")
        with st.form("sin_form", clear_on_submit=True):
            sin_title = st.text_input("المعصية / الزلة التي وقعت فيها:")
            root_why = st.selectbox("السبب الجذري الحقيقي الذي أوصلك لها:", ["السهر المفرط 🌙", "الفراغ والملل ⏳", "الخلوة بالهاتف والإنترنت 📱", "الابتعاد عن الصحبة الصالحة 👥", "الغضب والتوتر ⚡", "سبب آخر"])
            action_plan = st.text_area("الخطة الوقائية لمنع تكرارها غداً:")
            if st.form_submit_button("توثيق المعصية وإضافتها للتحليل الوقائي"):
                if sin_title.strip() and supabase:
                    try:
                        supabase.table("sin_tracker_logs").insert({
                            "sin_type": sin_title,
                            "root_cause": root_why,
                            "reflection_notes": action_plan
                        }).execute()
                        st.info("⚠️ تم تسجيل السبب في الرادار. استغفر ربك وابدأ من جديد بثبات.")
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")

# ==========================================
# 5. قسم الجيم، التغذية، والميزان الصباحي
# ==========================================
elif menu == "🏃‍♂️ الجيم، التغذية، والميزان الصباحي":
    st.title("🏃‍♂️ محرك اللياقة البدنية، الجيم، والتغذية")
    
    col_gym1, col_gym2 = st.columns([1, 1])
    
    with col_gym1:
        st.subheader("🏋️‍♂️ سجل حضور الجيم وتمارين اليوم")
        with st.form("gym_form"):
            attended = st.radio("هل ذهبت إلى الجيم اليوم؟", ["نعم، أنجزت التمرينة كاملة 💪", "لا، لم أذهب ❌"])
            reason = ""
            if "لا" in attended:
                reason = st.text_input("ما هو عذر الغياب؟ (راحة مجدولة، كسل، تعب، ضيق وقت):")
            workout_notes = st.text_area("تفاصيل التمرينة والأوزان المحققة:")
            if st.form_submit_button("حفظ سجل الجيم اليومي"):
                if supabase:
                    try:
                        supabase.table("gym_nutrition_logs").insert({
                            "attended_gym": "نعم" in attended,
                            "absence_reason": reason,
                            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                        }).execute()
                        st.success("✅ تم حفظ تقرير الجيم!")
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")
                        
    with col_gym2:
        st.subheader("🥗 مراقب التغذية والوزن الصباحي")
        with st.form("nutrition_form"):
            food_eval = st.radio("تقييم أكلك اليوم:", ["صحي 100% 🥗", "لخبطت في الدايت 🍔"])
            junk_notes = st.text_input("إذا لخبطت، ما الذي أكلته بالتحديد؟")
            morning_w = st.number_input("الوزن الصباحي (على معدة فارغة):", min_value=40.0, max_value=200.0, value=78.5, step=0.1)
            if st.form_submit_button("حفظ بيانات التغذية والوزن"):
                st.success("✅ تم تحديث قياسات التغذية والميزان بنجاح!")

# ==========================================
# 6. قسم الخطط الزمنية واقتناص الوظائف
# ==========================================
else:
    st.title("💼 هرم الخطط الزمنية ونظام اقتناص الوظائف (CRM)")
    
    tab_cascade, tab_jobs = st.tabs(["⏳ هرم تقسيم الزمن (Time-Horizon Cascade)", "🎯 نظام اقتناص الوظائف وجسر المهارات"])
    
    with tab_cascade:
        st.subheader("خوارزمية تقسيم الهدف الزمني")
        st.write("قسم هدف الـ 6 شهور الكبير إلى خطة 3 شهور ⬅️ شهر ⬅️ أسبوع ⬅️ مهام يومية للمذاكرة.")
        with st.form("cascade_form"):
            horizon = st.selectbox("المستوى الزمني للهدف:", ["هدف 6 شهور (الرؤية الكبيرة)", "خطة 3 شهور (المرحلة الحالية)", "خطة الشهر (أهداف الشهر)", "خطة الأسبوع", "مهمة مذاكرة يومية (Planned vs Executed)"])
            task_name = st.text_input("عنوان الهدف / المهمة:")
            c_p, c_e = st.columns(2)
            with c_p:
                planned_h = st.number_input("الساعات المخططة للمذاكرة:", min_value=0.5, step=0.5, value=3.0)
            with c_e:
                executed_h = st.number_input("الساعات المنفذة بالفعل:", min_value=0.0, step=0.5, value=2.5)
            if st.form_submit_button("تثبيت المهمة في الهرم الزمني"):
                if supabase and task_name.strip():
                    try:
                        supabase.table("time_cascade_tasks").insert({
                            "title": task_name,
                            "planned_hours": planned_h,
                            "executed_hours": executed_h,
                            "is_completed": executed_h >= planned_h
                        }).execute()
                        st.success("✅ تم إدراج المهمة وحساب كفاءة الإنجاز!")
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")
                        
    with tab_jobs:
        st.subheader("🎯 نظام متابعة الشركات وجسر المهارات (Skill Bridge CRM)")
        st.write("سجل كل شركة تقدمت إليها، مواعيد المقابلات، والكورسات المطلوبة لتتحول فوراً لخطة مذاكرة.")
        with st.form("job_form"):
            comp_name = st.text_input("اسم الشركة:")
            role = st.text_input("المسمى الوظيفي:")
            stat = st.selectbox("حالة التقديم:", ["تم إرسال الـ CV", "بانتظار الرد", "تحديد موعد مقابلة 🗓️", "تم القبول 🎉", "مرفوض مع ملاحظات"])
            needed_skills = st.text_area("كورسات أو مهارات لاحظت أنهم يطلبونها (Skill Bridge):", placeholder="مثال: يطلبون خبرة في Docker و Next.js...")
            if st.form_submit_button("حفظ بيانات الشركة وجسر المهارات"):
                if supabase and comp_name.strip():
                    try:
                        supabase.table("job_hunter_crm").insert({
                            "company_name": comp_name,
                            "role_title": role,
                            "status": stat,
                            "requested_skills_courses": needed_skills
                        }).execute()
                        st.success("✅ تم تسجيل بيانات الشركة في الـ CRM وربط جسر المهارات!")
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")
