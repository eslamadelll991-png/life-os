import streamlit as st
import time

# إعداد الصفحة لتكون بملء الشاشة وإخفاء القوائم
st.set_page_config(page_title="رحلة عمرنا", page_icon="✨", layout="centered")

# دمج CSS متقدم لعمل الأنيميشن (أوراق الشجر) والتصميم الزجاجي والخطوط
st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Amiri', serif;
        direction: rtl;
        text-align: center;
        background: linear-gradient(180deg, #0f2027, #203a43, #2c5364); /* خلفية ليلية رومانسية */
        color: #f8fafc;
        scroll-behavior: smooth;
    }
    
    /* إخفاء علامات Streamlit العلوية والسفلية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* أنيميشن أوراق الشجر المتساقطة */
    .leaf {
        position: fixed;
        top: -50px;
        font-size: 28px;
        user-select: none;
        pointer-events: none;
        z-index: 0;
        animation: fall linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(-50px) rotate(0deg); opacity: 1; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }
    
    /* تصميم الكروت الزجاجية (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px 30px;
        margin: 30px auto;
        max-width: 700px;
        z-index: 10;
        position: relative;
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px 0 rgba(254, 202, 87, 0.2);
    }
    
    /* خطوط العناوين والقصائد */
    .year-title {
        font-family: 'Aref Ruqaa', serif;
        color: #feca57; /* لون ذهبي */
        font-size: 38px;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .poem-text {
        font-size: 24px;
        line-height: 2;
        color: #f1f2f6;
    }
    
    /* تصميم زر البداية */
    .stButton>button {
        background: transparent !important;
        border: 2px solid #feca57 !important;
        color: #feca57 !important;
        font-family: 'Aref Ruqaa', serif;
        font-size: 24px !important;
        border-radius: 50px !important;
        padding: 10px 40px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: #feca57 !important;
        color: #0f2027 !important;
        transform: scale(1.05);
    }
</style>

<!-- توليد الأوراق المتساقطة في الخلفية بسرعات وأماكن مختلفة -->
<div class="leaf" style="left: 10%; animation-duration: 12s; animation-delay: 0s;">🍂</div>
<div class="leaf" style="left: 20%; animation-duration: 15s; animation-delay: 2s;">🍁</div>
<div class="leaf" style="left: 30%; animation-duration: 11s; animation-delay: 4s;">🍃</div>
<div class="leaf" style="left: 45%; animation-duration: 18s; animation-delay: 1s;">🍂</div>
<div class="leaf" style="left: 60%; animation-duration: 14s; animation-delay: 5s;">🍁</div>
<div class="leaf" style="left: 75%; animation-duration: 16s; animation-delay: 3s;">🍃</div>
<div class="leaf" style="left: 85%; animation-duration: 13s; animation-delay: 6s;">🍂</div>
<div class="leaf" style="left: 95%; animation-duration: 17s; animation-delay: 2s;">🍁</div>
''', unsafe_allow_html=True)

# إدارة حالة التطبيق (هل تم الضغط على زر البداية أم لا؟)
if 'started' not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    # شاشة البداية (بوابة الدخول)
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: "Aref Ruqaa", serif; color: #feca57; font-size: 60px;'>رحلة عمركِ 🍂</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #c8d6e5; margin-bottom: 40px; font-weight: normal;'>هل أنتي مستعدة لفتح الهدية؟</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("اضغطي لتبدأي الرحلة ✨", use_container_width=True):
            st.session_state.started = True
            st.rerun()
else:
    # المشهد الثاني: الرحلة والموسيقى
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><p style='color: #feca57; font-size: 18px;'>🎶 شغلي الموسيقى وانزلي ببطء لتقرأي رحلتك..</p></div>", unsafe_allow_html=True)
    
    # مشغل الموسيقى (يجب وضع ملف music.mp3 في نفس مجلد GitHub)
    try:
        st.audio("music.mp3", format="audio/mp3", start_time=0)
    except:
        st.warning("⚠️ ملحوظة: ملف الموسيقى غير موجود. يرجى رفع ملف باسم 'music.mp3' على GitHub.")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # قائمة الرسائل الـ 23
    messages = [
        ("العام الأول", "ميلادُ النورِ في عينيكِ، فجرٌ أشرقَ في الدنيا ليضيءَ أيامي الآتية."),
        ("العام الثاني", "خطوتكِ الأولى على الأرض، زرعت في الكونِ ياسمينًا لا يذبل."),
        ("العام الثالث", "ضحكتكِ الطفولية، أولُ أغنيةٍ عرفتها العصافير وحفظتها عن ظهر قلب."),
        ("العام الرابع", "تعلّمَ الوردُ في هذا العام كيف يستمدُّ لونه من حُمرةِ وجنتيكِ."),
        ("العام الخامس", "براءةٌ تسكنُ ملامحكِ، جعلتِ الملائكةَ تحرسُ أحلامكِ الرقيقة."),
        ("العام السادس", "كبرتِ قليلًا، وصار للشمسِ منافسٌ حقيقيٌ في الإشراق والدفء."),
        ("العام السابع", "سبعُ سماواتٍ من الرقةِ تجمّعت واستقرت في قلبكِ الصغير."),
        ("العام الثامن", "كفراشةٍ تلوّنُ الحياة، بدأ سحركِ ينبضُ ويزهر في كل الأرجاء."),
        ("العام التاسع", "تسعةُ أقمارٍ تدورُ حولكِ، تستمدُّ من بهائكِ الضياء والسحر."),
        ("العام العاشر", "أولُ عقدٍ من الزمان، اكتملت فيه لوحةُ طفولتكِ البهية كقطعةِ سكر."),
        ("العام الحادي عشر", "بدايةُ الصِبا، كغصنِ بانٍ يتمايلُ بخفةٍ مع نسيمِ الصباح."),
        ("العام الثاني عشر", "كبرتِ وكبرَ الحلا، وصار وجهكِ قصيدةً تتغنى بها الأيام."),
        ("العام الثالث عشر", "قمرٌ يتململُ في كبد السماء، يغارُ من فتاةٍ تزدادُ حسنًا كل يوم."),
        ("العام الرابع عشر", "ربيعٌ دائمٌ يسكنُ أنفاسكِ، وتزهرُ الأرضُ أينما حلّت خطاكِ."),
        ("العام الخامس عشر", "نصفُ قمرٍ، ونصفُ شمسٍ، وجمالٌ حائرٌ لا يُقاسُ بالكلمات."),
        ("العام السادس عشر", "رقةٌ ودلال، كأنكِ خُلقتِ من قطراتِ الندى وماءِ الورد."),
        ("العام السابع عشر", "أنوثةٌ تتفتحُ كزهرةِ أوركيد، نادرة، ساحرة، وتخطف الأنفاس."),
        ("العام الثامن عشر", "اكتملَ البدرُ، وصارت الصبيةُ سيدةً تسرقُ الألباب وتأسر الروح."),
        ("العام التاسع عشر", "في عينيكِ بحرٌ من الشغف، وفي ابتسامتكِ وطنٌ ألجأ إليه."),
        ("العام العشرون", "عقدانِ من السحرِ، كلُّ عامٍ فيكِ كان أجملُ من ألفِ عامٍ مما يعُدّون."),
        ("العام الحادي والعشرون", "تتوّجتِ أميرةً على عرشِ قلبي، سيدةً لكل تفاصيلي وأيامي."),
        ("العام الثاني والعشرون", "نضجٌ ورقة، عقلٌ يزنُ الدنيا، وقلبٌ حنون يسعُ الكون بأسره."),
        ("العام الثالث والعشرون", "هنا والآن، أنتِ أجملُ ما في العمرِ، وكلُّ سنيني لكِ فداءٌ وحب.")
    ]
    
    # عرض البطاقات بأسلوب سحري
    for idx, (year, text) in enumerate(messages):
        st.markdown(f'''
        <div class="glass-card">
            <div class="year-title">🍂 {year}</div>
            <div class="poem-text">{text}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # مسافة بين كل كارت والتاني عشان التمرير (Scrolling) ياخد وقته
        if idx < len(messages) - 1:
            st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
            
    # الخاتمة (الزهرة تتفتح)
    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)
    st.markdown('''
    <div style="background: rgba(254, 202, 87, 0.15); border: 2px solid #feca57; border-radius: 20px; padding: 60px 30px; text-align: center; box-shadow: 0 0 40px rgba(254, 202, 87, 0.4); margin-bottom: 100px;">
        <h1 style="font-family: 'Aref Ruqaa', serif; color: #feca57; font-size: 55px; margin-bottom: 30px;">🌸 كل عام وأنتِ ملكتي 🌸</h1>
        <h3 style="color: #fff; line-height: 2; font-weight: normal; font-size: 26px;">كل سنة وأنتي أجمل وأغلى حاجة في حياتي.<br>العمر كله وإحنا سوا يا روح قلبي.</h3>
    </div>
    ''', unsafe_allow_html=True)
