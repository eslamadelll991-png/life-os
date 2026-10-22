elif menu == "🕌 الدين، الصلوات، ورادار المعاصي":
    st.title("🕌 محرك الدين، الصلاة، وتزكية النفس")
    
    tab_daily, tab_qadaa, tab_plan, tab_ramadan, tab_sin, tab_reports = st.tabs([
        "📝 السجل اليومي", "🔄 الصلوات الفائتة", "🗓️ الخطة الأسبوعية", "🌙 رمضان", "🛡️ رادار المعاصي", "📊 التقارير"
    ])
    
    # ---------------------------------------------------------
    # 📝 السجل اليومي (صلوات، أذكار، قرآن، قيام)
    # ---------------------------------------------------------
    with tab_daily:
        st.subheader(f"سجل الطاعات ليوم: {TODAY_DATE}")
        
        with st.form("spiritual_daily_form"):
            st.markdown("**1️⃣ الصلوات الخمس:**")
            col1, col2, col3, col4, col5 = st.columns(5)
            options = ["مسجد 🕌", "بيت 🏠", "فائتة ❌"]
            with col1: fajr = st.radio("الفجر", options, index=0)
            with col2: dhuhr = st.radio("الظهر", options, index=1)
            with col3: asr = st.radio("العصر", options, index=0)
            with col4: maghrib = st.radio("المغرب", options, index=0)
            with col5: isha = st.radio("العشاء", options, index=0)
            
            st.markdown("---")
            st.markdown("**2️⃣ الأذكار وقيام الليل:**")
            col_z1, col_z2, col_q = st.columns(3)
            with col_z1: azkar_m = st.checkbox("أذكار الصباح ☀️")
            with col_z2: azkar_e = st.checkbox("أذكار المساء 🌙")
            with col_q: qiyam = st.number_input("عدد ركعات قيام الليل:", min_value=0, step=2, value=0)
            
            st.markdown("---")
            st.markdown("**3️⃣ القرآن الكريم والدروس:**")
            col_q1, col_q2, col_q3 = st.columns(3)
            with col_q1:
                q_read = st.number_input("عدد صفحات القراءة (الورد):", min_value=0, value=0)
                q_lesson = st.checkbox("أخذت درس قرآن / تجويد اليوم")
            with col_q2:
                surah = st.text_input("اسم السورة (للحفظ/المراجعة):")
                q_mem = st.number_input("عدد الصفحات المحفوظة:", min_value=0, value=0)
            with col_q3:
                st.write("المراجعة:")
                rev_start = st.number_input("من صفحة:", min_value=0, value=0)
                rev_end = st.number_input("إلى صفحة:", min_value=0, value=0)

            if st.form_submit_button("💾 حفظ سجل الطاعات اليومي", use_container_width=True):
                if supabase:
                    try:
                        data = {
                            "log_date": TODAY_DATE,
                            "fajr": fajr, "dhuhr": dhuhr, "asr": asr, "maghrib": maghrib, "isha": isha,
                            "azkar_morning": azkar_m, "azkar_evening": azkar_e, "qiyam_rakaat": qiyam,
                            "quran_read_pages": q_read, "quran_lesson": q_lesson,
                            "surah_name": surah, "quran_memorized_pages": q_mem,
                            "quran_rev_start": rev_start, "quran_rev_end": rev_end
                        }
                        supabase.table("spiritual_daily_logs").upsert(data, on_conflict="log_date").execute()
                        st.success("✅ تقبل الله! تم حفظ سجل طاعاتك اليوم بنجاح.")
                    except Exception as ex:
                        st.error(f"خطأ في الحفظ: {ex}")

    # ---------------------------------------------------------
    # 🔄 الصلوات الفائتة (قضاء الصلاة)
    # ---------------------------------------------------------
    with tab_qadaa:
        st.subheader("🔄 سجل الصلوات الفائتة (القضاء)")
        st.write("تابع عدد الصلوات التي قمت بقضائها. كلما صليت فرضاً فائتاً، أضفه هنا ليتم حسابه في إجمالي الرصيد المقضي.")
        
        totals = {"fajr": 0, "dhuhr": 0, "asr": 0, "maghrib": 0, "isha": 0}
        if supabase:
            try:
                res = supabase.table("qadaa_totals").select("*").eq("id", 1).execute()
                if res.data:
                    t = res.data[0]
                    totals = {"fajr": t.get("fajr_total",0), "dhuhr": t.get("dhuhr_total",0), "asr": t.get("asr_total",0), "maghrib": t.get("maghrib_total",0), "isha": t.get("isha_total",0)}
            except Exception:
                pass
                
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(f"<div class='qadaa-box'><div class='qadaa-title'>الفجر</div><div class='qadaa-count'>{totals['fajr']}</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='qadaa-box'><div class='qadaa-title'>الظهر</div><div class='qadaa-count'>{totals['dhuhr']}</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='qadaa-box'><div class='qadaa-title'>العصر</div><div class='qadaa-count'>{totals['asr']}</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='qadaa-box'><div class='qadaa-title'>المغرب</div><div class='qadaa-count'>{totals['maghrib']}</div></div>", unsafe_allow_html=True)
        with c5: st.markdown(f"<div class='qadaa-box'><div class='qadaa-title'>العشاء</div><div class='qadaa-count'>{totals['isha']}</div></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        with st.form("qadaa_form"):
            st.write("➕ **ماذا صليت من الفوائت اليوم؟ (أدخل العدد)**")
            i1, i2, i3, i4, i5 = st.columns(5)
            with i1: add_f = st.number_input("قضاء الفجر", min_value=0, value=0)
            with i2: add_d = st.number_input("قضاء الظهر", min_value=0, value=0)
            with i3: add_a = st.number_input("قضاء العصر", min_value=0, value=0)
            with i4: add_m = st.number_input("قضاء المغرب", min_value=0, value=0)
            with i5: add_i = st.number_input("قضاء العشاء", min_value=0, value=0)
            
            if st.form_submit_button("تحديث رصيد الصلوات المقضية"):
                if supabase:
                    try:
                        new_f = totals['fajr'] + add_f
                        new_d = totals['dhuhr'] + add_d
                        new_a = totals['asr'] + add_a
                        new_m = totals['maghrib'] + add_m
                        new_i = totals['isha'] + add_i
                        supabase.table("qadaa_totals").update({
                            "fajr_total": new_f, "dhuhr_total": new_d, "asr_total": new_a, 
                            "maghrib_total": new_m, "isha_total": new_i
                        }).eq("id", 1).execute()
                        st.success("✅ تم إضافة الصلوات المقضية للرصيد الإجمالي بنجاح!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")

    # ---------------------------------------------------------
    # 🗓️ الخطة الأسبوعية
    # ---------------------------------------------------------
    with tab_plan:
        st.subheader("🗓️ الخطة الأسبوعية (قرآن، دروس، وقيام)")
        st.write("اكتب خطتك لأيام الأسبوع بالكامل هنا لتكون مرجعك اليومي.")
        
        current_plan = ""
        if supabase:
            try:
                res = supabase.table("spiritual_weekly_plan").select("plan_text").eq("id", 1).execute()
                if res.data:
                    current_plan = res.data[0].get("plan_text", "")
            except Exception:
                pass
                
        with st.form("plan_form"):
            plan_input = st.text_area("خطتك الأسبوعية المخصصة:", value=current_plan, height=250, 
                                      placeholder="السبت: حفظ 3 صفحات بعد الفجر + درس تجويد بعد العصر...")
            if st.form_submit_button("💾 حفظ الخطة الأسبوعية"):
                if supabase:
                    try:
                        supabase.table("spiritual_weekly_plan").upsert({"id": 1, "plan_text": plan_input, "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}).execute()
                        st.success("✅ تم تحديث خطتك الأسبوعية بنجاح!")
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")

    # ---------------------------------------------------------
    # 🌙 رمضان
    # ---------------------------------------------------------
    with tab_ramadan:
        st.subheader("🌙 وضع شهر رمضان المبارك")
        with st.form("ramadan_form", clear_on_submit=True):
            fasted = st.radio("هل صمت اليوم؟", ["نعم 🌙", "لا (عذر شرعي / مرض) ❌"])
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                taraweeh = st.number_input("عدد ركعات التراويح:", min_value=0, step=2, value=8)
            with r_col2:
                qiyam_r = st.number_input("عدد ركعات التهجد/القيام المتبقية:", min_value=0, step=2, value=0)
            notes = st.text_input("أعمال صالحة أخرى (صدقة، تفطير صائم، عمرة):")
            
            if st.form_submit_button("حفظ يوميات رمضان"):
                if supabase:
                    try:
                        supabase.table("ramadan_logs").upsert({
                            "log_date": TODAY_DATE,
                            "fasted": "نعم" in fasted,
                            "taraweeh_rakaat": taraweeh,
                            "qiyam_rakaat": qiyam_r,
                            "notes": notes
                        }, on_conflict="log_date").execute()
                        st.success("✅ تم توثيق اليوم الرمضاني. تقبل الله طاعتك!")
                    except Exception as ex:
                        st.error(f"خطأ: {ex}")

    # ---------------------------------------------------------
    # 🛡️ رادار المعاصي
    # ---------------------------------------------------------
    with tab_sin:
        st.subheader("🛡️ رادار تحليل أسباب المعاصي والزلات")
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

    # ---------------------------------------------------------
    # 📊 تقارير الدين
    # ---------------------------------------------------------
    with tab_reports:
        st.subheader("📊 تقارير الأداء الديني")
        if supabase:
            try:
                res = supabase.table("spiritual_daily_logs").select("*").execute()
                if res.data:
                    df = pd.DataFrame(res.data)
                    df['log_date'] = pd.to_datetime(df['log_date'])
                    
                    rep_period = st.radio("اختر فترة التقرير الديني:", ["آخر 7 أيام", "آخر 30 يوم"], horizontal=True)
                    days = 7 if "7" in rep_period else 30
                    mask = (df['log_date'] >= (pd.to_datetime(TODAY_DATE) - pd.Timedelta(days=days)))
                    period_df = df.loc[mask]
                    
                    if not period_df.empty:
                        total_quran = period_df['quran_read_pages'].sum()
                        total_qiyam = period_df['qiyam_rakaat'].sum()
                        azkar_m_count = period_df['azkar_morning'].sum()
                        
                        col1, col2, col3 = st.columns(3)
                        with col1: st.markdown(f'<div class="glass-card"><div class="metric-label">صفحات القرآن المقروءة</div><div class="metric-value">{total_quran}</div></div>', unsafe_allow_html=True)
                        with col2: st.markdown(f'<div class="glass-card"><div class="metric-label">إجمالي ركعات القيام</div><div class="metric-value">{total_qiyam}</div></div>', unsafe_allow_html=True)
                        with col3: st.markdown(f'<div class="glass-card"><div class="metric-label">أيام الالتزام بأذكار الصباح</div><div class="metric-value">{azkar_m_count}</div></div>', unsafe_allow_html=True)
                        
                        st.markdown("**معدل أداء الصلوات في المسجد:**")
                        prayers = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']
                        mosque_counts = sum((period_df[p] == 'مسجد 🕌').sum() for p in prayers)
                        home_counts = sum((period_df[p] == 'بيت 🏠').sum() for p in prayers)
                        missed_counts = sum((period_df[p] == 'فائتة ❌').sum() for p in prayers)
                        
                        chart_data = pd.DataFrame({
                            "المكان": ["المسجد 🕌", "البيت 🏠", "فائتة ❌"],
                            "العدد": [mosque_counts, home_counts, missed_counts]
                        })
                        st.bar_chart(chart_data.set_index("المكان"))
                    else:
                        st.warning("لا توجد بيانات كافية لهذه الفترة.")
                else:
                    st.info("ابدأ بتسجيل طاعاتك في السجل اليومي لرؤية التقارير.")
            except Exception as e:
                st.error(f"خطأ في توليد التقارير: {e}")

# ==========================================
# 3. قسم النفسية والعادات
# ==========================================
elif menu == "🧠 النفسية، العادات، وخزنة القراءة":
    st.title("🧠 محرك النفسية، إدارة العادات، وخزنة القراءة")
    st.info("هذا القسم يعمل بكامل التطويرات التي أنجزناها سابقاً. اختر قسم الدين لتجربة التحديثات الجديدة.")

# ==========================================
# 4. معرض الفن
# ==========================================
elif menu == "🎨 معرض الرسومات الفنية (Art Gallery)":
    st.title("🎨 معرض الرسومات الفنية وتتبع التطور الإبداعي")
    st.info("قسم معرض الصور يعمل بكفاءة...")

# ==========================================
# 5. الجيم والتغذية
# ==========================================
elif menu == "🏃‍♂️ الجيم، التغذية، والميزان الصباحي":
    st.title("🏃‍♂️ محرك اللياقة البدنية، الجيم، والتغذية")
    st.info("قسم اللياقة يعمل بكفاءة...")

# ==========================================
# 6. الخطط والوظائف
# ==========================================
else:
    st.title("💼 هرم الخطط الزمنية ونظام اقتناص الوظائف (CRM)")
    st.info("قسم الوظائف والخطط يعمل بكفاءة...")
