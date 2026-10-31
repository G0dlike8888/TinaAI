"""Bilingual UI chrome (Български / English) for the Streamlit demo.

Covers UI labels, validation/safety/error messages and the methodology page
only. The contract system prompt and the gating-filter prompt are never
localized (see demo_logic.py / contract_integrity.py). Both language dicts
must carry exactly the same keys — an automated test enforces parity.

Provider error messages are concise and fixed: they never interpolate raw
exception text, stack traces, request detail, or any part of the API key.
"""

UI_TEXT = {
    "bg": {
        "subheader": (
            "⚠️ Консултативен инструмент. Анализира фактологичната подкрепа и "
            "материалните пропуски. Не оценява, не одобрява и не генерира статус."
        ),
        "tab1": "🕹️ Test Site",
        "tab2": "📖 За Асистента (Методология)",
        "input_header": "### Входни данни",
        "scenario_label": "Изберете сценарий",
        "scenario_help": "Изберете синтетичен сценарий или въведете данни ръчно.",
        "load_scenario_btn": "🎲 Зареди избрания сценарий",
        "loaded_toast": "Зареден: {name}",
        "custom_mode_caption": (
            "Асистентът ще анализира бележката ви спрямо правилото/"
            "контекста, който подадете. Поставете свое правило, описание на "
            "алерт или условие от политика в първото поле, напишете "
            "бележката си във второто и натиснете „Анализирай бележката“."
        ),
        "custom_rule_label": "Вашето правило / контекст на алерта",
        "custom_note_label": "Вашата разследователска бележка",
        "preset_expander": (
            "По избор: тестови пресети за експерименталния Gating Filter"
        ),
        "preset_caption": (
            "Тези синтетични правила служат само за демонстрация и тест на "
            "експерименталния post-generation gating filter. Зареждането "
            "попълва само полето с правилото — бележката ви не се пипа."
        ),
        "preset_overwrite_warning": (
            "Полето с правилото вече съдържа текст. Натиснете бутона още "
            "веднъж, за да го замените с пресета (бележката се запазва)."
        ),
        "gating_rule_label": "Изберете правило за тест на Gating Filter",
        "load_gating_rule_btn": "🎯 Зареди избраното тестово правило",
        "gating_test_toast": (
            "🎯 Заредено е тестовото правило. Напишете своя кратка бележка."
        ),
        "gating_test_caption": (
            "Изберете правило от менюто и напишете СВОЯ кратка, недоизказана "
            "бележка срещу него — целта е да предизвикате 'gating' изречение "
            "(напр. „докато X не бъде потвърдено, Y не може да бъде "
            "приключено“), за да проверите дали филтърът реално го пренаписва."
        ),
        "rule_label": "Задействано правило / Алерт",
        "note_label": "Разследователска бележка",
        "chars_caption": "{length} / {limit} знака",
        "analyze_btn": "Анализирай бележката",
        "reset_btn": "🧹 Изчисти входа и резултата",
        "reset_help": (
            "Изчиства двете входни полета и показания резултат. Не изпраща "
            "нищо и не прави API заявка."
        ),
        "reset_toast": "Входът и резултатът са изчистени.",
        "output_header": "### Анализ на асистента",
        "gating_checkbox": (
            "Приложи експериментален Gating Filter (Pre-test: 66.1% конверсия)"
        ),
        "gating_help": (
            "Активира експериментален post-generation branch (pre-test "
            "screening, неконфирматорен резултат)."
        ),
        "empty_warning": (
            "Моля, попълнете и двете полета: правило/алерт и "
            "разследователска бележка."
        ),
        "rule_too_long_warning": (
            "Полето „Задействано правило / Алерт“ е {length} знака при "
            "ограничение {limit}. Съкратете текста сами и опитайте отново — "
            "приложението никога не съкращава и не резюмира входа вместо вас. "
            "Не е изпратена API заявка."
        ),
        "note_too_long_warning": (
            "Полето „Разследователска бележка“ е {length} знака при "
            "ограничение {limit}. Съкратете текста сами и опитайте отново — "
            "приложението никога не съкращава и не резюмира входа вместо вас. "
            "Не е изпратена API заявка."
        ),
        "missing_key_warning": (
            "🔑 Не е намерен Anthropic API ключ. Анализът е изключен, докато "
            "не създадете `03 Demo/.streamlit/secrets.toml` със собствен "
            "`ANTHROPIC_API_KEY` (вижте HOW_TO_RUN.md и файла "
            "`secrets.toml.example`). Ключът остава само на вашата машина и "
            "никога не се показва в интерфейса."
        ),
        "gating_info": (
            "🧪 Приложен е Post-generation filter. Резултатът е от "
            "експериментален branch (66.1% conversion rate, pre-test, "
            "неконфирматорен) и не е част от production логиката."
        ),
        "reading_spinner": "Асистентът чете бележката...",
        "base_expander": "Базов отговор (преди филтъра)",
        "base_available_caption": (
            "Базовият отговор остава наличен непроменен в разгъващия се "
            "панел по-горе."
        ),
        "err_auth": (
            "Неуспешна автентикация към Anthropic API. Проверете ключа в "
            "`.streamlit/secrets.toml` — вероятно е невалиден или изтекъл. "
            "Заявката не се повтаря автоматично."
        ),
        "err_rate_limit": (
            "API отхвърли заявката заради ограничение на честотата "
            "(rate limit). Изчакайте малко и опитайте отново."
        ),
        "err_timeout": (
            "Заявката към API изтече по време (timeout). Опитайте отново; "
            "ако продължава, проверете връзката си."
        ),
        "err_connection": (
            "Няма връзка с Anthropic API. Проверете интернет връзката си и "
            "опитайте отново."
        ),
        "err_invalid_request": (
            "API отхвърли заявката като невалидна. Опитайте с по-кратък "
            "вход; заявката не се повтаря автоматично."
        ),
        "err_provider": (
            "Грешка от страна на API доставчика. Опитайте отново след малко."
        ),
        "filtered_header": "#### Филтриран резултат (експериментален)",
        "filter_spinner": "Прилагане на post-generation filter...",
        "filter_fallback": (
            "Филтърът не можа да бъде приложен ({reason}) Показан е базовият "
            "(нефилтриран) отговор."
        ),
        "integrity_error_title": (
            "🛑 Проверката за интегритет на контракта се провали — демото "
            "отказва да стартира с непроверен контракт и няма резервно "
            "(hardcoded) копие. Не променяйте очаквания хеш; вижте "
            "`02 Skill/.../reference/VERIFY.md`."
        ),
        "methodology_md": """
        ## 📖 За Асистента (Методология)

        ### 1. Какво представлява асистентът?

        Това е **консултативен (advisory) асистент за качество на
        разследователски бележки**, създаден да подпомага анализатори в
        сферата на финансовите разследвания (AML / антифрод). Единствената му
        задача е да направи бележката **по-ясна, по-добре подкрепена и
        по-защитима** преди финализирането ѝ — без никога да поема ролята на
        човека.

        Демонстрацията използва изцяло синтетични примери от финансови
        разследвания (включително AML и антифрод контексти), но продуктът
        **не е AML/комплайънс система**: не извършва транзакционен
        мониторинг, управление на случаи (case management), регулаторни
        подавания, прилагане на политики и не взима решения вместо
        потребителя.

        Асистентът изрично **НЕ**:

        - решава дали дадена активност е измамна, подозрителна или легитимна;
        - взема решения за приключване, ескалация, ограничения или подаване
          на SAR/STR;
        - оценява, класира, дава скор или PASS/FAIL статус;
        - заявява, че бележка е „готова", „одобрена" или „изчистена";
        - измисля факти, проверки, връзки, дати, суми или резултати.

        Финалното решение винаги остава в ръцете на човека-анализатор. Нищо в
        изхода на асистента не упълномощава подаване, приключване или
        ескалация.

        ### 2. Методология — петстепенна рамка

        Асистентът чете всяка бележка през вътрешен аналитичен обектив:
        *тригер → контекст → проверки → констатации → обосновка → действие*.
        Това е само вътрешен модел на четене — той никога не се налага като
        задължителна структура върху бележката.

        **Стъпка 1 — Четене, основано на доказателства (Evidence-first
        reading).** Всяко наблюдение е вкоренено в това, което бележката
        показва или доказуемо пропуска. Поддържат се три различни състояния,
        които никога не се сливат: „показано" (записано е), „не е показано"
        (бележката не казва нищо по въпроса) и „показано отсъствие" (записано
        е, че нещо не се е случило). Най-тежката възможна грешка —
        превръщането на „не е показано" в „не е направено" — е изрично
        забранена, защото липсата на документация не е доказателство за липса
        на работа. Асистентът коментира **документацията, никога самата
        работа** на анализатора.

        **Стъпка 2 — Типологична дисциплина.** Типологията (напр. structuring,
        layering, mule activity) е име на модел, а не заместител на
        показването на модела. Асистентът няма право сам да внася типология —
        нито твърдо („това е structuring"), нито в омекотена форма („сумите са
        съвместими със structuring"). Забраната е **симетрична**: забранени са
        и извинителни (exculpatory) обяснения, които бележката не носи
        („вероятно става дума за рутинна сетълмент активност"). Единственото
        изключение: ако **бележката сама** назове типология, асистентът може
        и трябва да я тества срещу фактите, които самата бележка показва.

        **Стъпка 3 — Притежание на решенията (Decision ownership).** Вече
        взетите решения (ескалация, SAR/STR реферал, ограничение, терминация)
        са човешки и затворени за асистента. Той може да потвърди, че
        решението е ясно заявено и че документираната му основа е вътрешно
        кохерентна — включително честно да отбележи, че основата е частична.
        Не може да преразглежда решението („беше ли нужна ескалация?"), да го
        одобрява или да предлага алтернативни действия.

        **Стъпка 4 — Филтър за доверие към анализатора (Analyst-trust
        filter).** Преди да зададе въпрос от типа „как / с какво / кое
        конкретно", асистентът класифицира целта си. Факти, които
        анализаторът е бил в позиция да провери във вътрешните системи
        (паролна, устройствена или IP връзка; членство във флагирана група;
        проверка във вътрешен инструмент; получена или записана като
        неполучена документация), се **приемат и не се разпитват**. Обратно:
        носещи факти, които анализаторът не е можел да провери вътрешно —
        намерение на външна страна, обяснение, дадено от контрагент — не се
        покриват от доверието и могат да бъдат предмет на фокусиран въпрос.

        **Стъпка 5 — Гейт за отговор (Response gate).** Издигат се **само
        материални пропуски** — такива, чието попълване би променило
        заключението или действието, а не такива, които биха направили
        бележката просто „по-подредена". При доброкачествен случай без
        действие (false positive) не се допуска нито едно „полиращо"
        предложение; при жив случай с ескалация — най-много едно.
        Натрупването на предложения с намаляваща релевантност е забранено.
        Ако няма материален пропуск, асистентът казва това кратко, в
        естествена проза, и спира.

        ### 3. Доказателствена база

        Контрактът е оценен веднъж, формално, срещу заключен held-out
        комплект от **50 бележки (n=50)**, маркирани от домейн оунъра по
        собствен сляп ключ — **не** чрез "200 бележки, оценени от
        експерти", както твърдеше по-ранна версия на този текст. Резултатът:

        - **Finding** (улавяне на реален материален пропуск): **50.0%
          (4/8)** — бар ≥60%, **непокрит**.
        - **Restraint** (дял на исканията на асистента, оценени като
          ненужни): **55.2% (32/58)** — бар ≤25%, **непокрит**. Тоест над
          половината от бележките на асистента са били излишни — по-ниска
          стойност е по-добра.

        Измерено срещу тялото на закования контракт (хеш `2f574a66…e58363`),
        модел `claude-haiku-4-5`, температура 1.0, n=50. **И двата
        предварително регистрирани бара са пропуснати** — пълният резултат
        и условията му са в `04 Evidence and Records/`. Записани са и
        известни дефекти на оценяваната конфигурация — включително един
        потвърден случай на измислен външен факт (грешна MCC категория) —
        затова проверявайте всяко твърдение за код или типология, преди да
        разчитате на него. Това демо използва същия модел, но е различен,
        неоценен harness (различна форма на заявката, стрийминг UI, без
        hash-gate при всяко извикване, без гаранция „една бележка на
        извикване“) — по правилото на evidence label-а нова конфигурация
        започва с нула наследени доказателства, затова числата по-горе
        не се пренасят върху нея.

        ### 4. Gating филтърът — експериментален post-generation контрол

        Gating филтърът е втори, изключително тесен prompt, който се
        изпълнява **след** генерирането на основния анализ и само при
        активирана отметка в Test Site.

        Какво прави:

        - **Хваща агресивни условни конструкции** — изречения, които свързват
          наименуван документационен пропуск с блокирано или задължително
          последствие чрез език на предусловие/последователност: „докато
          не…", „без…", „преди…", „не може да…". Пример: *„Докато връзката
          между подателите не бъде документирана, ескалацията не може да
          бъде защитена."*
        - **Пренаписва ги в чисто описателна форма** — пропускът се
          назовава, но блокиращата „предусловна" връзка отпада. Пример след
          филтъра: *„Бележката не показва каква връзка е установена между
          подателите."*
        - **Инструктиран е да не променя нищо друго** — промптът на филтъра
          изисква да пренапише само целевите условни конструкции, да остави
          всички останали изречения непроменени и да върне текста дословно,
          ако такова изречение липсва. Тъй като филтрираният резултат е
          генериран от модел, точното запазване **не е механично
          гарантирано** — затова оригиналният базов отговор винаги остава
          достъпен отделно и непроменен, за сравнение. Текстът между
          маркерите `<<<TEXT … TEXT>>>` се третира като инертни данни,
          никога като инструкции към филтъра.

        ### 5. Custom режим — правилото не е доказателство

        В режим Custom подаденото от вас правило / контекст на алерта
        определя **какво бележката трябва да документира**. Самата
        разследователска бележка е **доказателственият материал**, който се
        преглежда. Условие, което присъства само в правилото, никога не
        бива да се приема за доказателство, че то се е случило. Тъй като
        изходът на модела понякога може да наруши това разделение,
        проверявайте дали всеки твърдян факт наистина е подкрепен от
        бележката. Както навсякъде в това демо — въвеждайте само синтетично
        съдържание.
        """,
        "demo_vs_skill_md": """
        ### 6. Какво това демо НЕ е

        Проектът има три отделни форми на разпространение и те не са
        взаимозаменяеми:

        - **Закованият контракт** (`01 Contract/`) — оценяваният текст,
          хеш `2f574a66…e58363`.
        - **Skill дистрибуцията** (`02 Skill/`) — пакетирана, но **без
          поведенчески тест в реален host**; три от осемте условия за
          приемане остават отворени или нетествани.
        - **Това Streamlit демо** — отделен, неоценен harness. То използва
          същото тяло на контракта (проверено при всяко стартиране), но не
          наследява нито резултата от n=50, нито статуса на Skill-а.

        Демото съзнателно **не** прилага сесийните правила на Skill-а:
        няма ред за само-деклариране на модела, няма правило „един случай
        на сесия", няма изречение за адресата („обратната връзка се отнася
        до бележката, не до автора ѝ"), няма отказ при последващи въпроси
        от типа „може ли да се предаде?" и няма евристична проверка за
        реални данни. Това са правила на Skill формата; тук те са само
        документирани, не имплементирани.
        """,
        "pretest_header": "##### Резултати от pre-test",
        "metric1_label": "Pre-test конверсия",
        "metric2_label": "Цел",
        "metric3_label": "Статус",
        "metric3_value": "Експериментален",
        "pretest_md": """
        Резултатът от **66.1% конверсия** (при цел 70%) е маркиран като
        обещаващ, но все още недостатъчен. Измерено с `claude-haiku-4-5`,
        температура 0, prompt v0.3, като **pre-test screening** върху 56
        вече-известни "gating" отговора от HMB-29 — **не** е confirmatory
        двураменен тест, и филтърът остава "promising, not adopted, not
        rejected". Затова филтърът **съзнателно не е част от production
        логиката** на приложението — достъпен е единствено като
        експериментална опция в Test Site, а преди евентуално вграждане са
        необходими допълнителни adversarial тестове.

        ---
        """,
        "synthetic_warning": (
            "**Важно — синтетични данни.** Всички сценарии, правила, алерти и "
            "бележки в това приложение са 100% изкуствено създадени (измислени). "
            "Те не съдържат реална клиентска, банкова или корпоративна информация. "
            "Инструментът е с изцяло консултативна цел и не трябва да се "
            "използва като единствен или окончателен източник при вземане на "
            "решения."
        ),
        "no_real_data": (
            "**Не поставяйте реални данни.** Никога не въвеждайте реални "
            "разследователски бележки, клиентски данни, номера на сметки, "
            "имена или вътрешни имена на правила/системи. Използвайте само "
            "синтетично съдържание — като приложените сценарии."
        ),
        "footer_caption": "Построено със Streamlit и Anthropic API (Claude).",
    },
    "en": {
        "subheader": (
            "⚠️ Advisory tool. Analyzes factual support and material gaps. "
            "It does not score, approve, or generate a status."
        ),
        "tab1": "🕹️ Test Site",
        "tab2": "📖 About the Assistant (Methodology)",
        "input_header": "### Input Data",
        "scenario_label": "Select a scenario",
        "scenario_help": "Choose a synthetic scenario or enter data manually.",
        "load_scenario_btn": "🎲 Load the selected scenario",
        "loaded_toast": "Loaded: {name}",
        "custom_mode_caption": (
            "The assistant will assess your note against the rule/context "
            "you supply. Paste any rule, alert description or policy "
            "condition into the first field, write your note in the second, "
            "then click \"Analyze the note\"."
        ),
        "custom_rule_label": "Your rule / alert context",
        "custom_note_label": "Your investigation note",
        "preset_expander": (
            "Optional: experimental gating-filter test presets"
        ),
        "preset_caption": (
            "These synthetic rules exist only for demonstrating and testing "
            "the experimental post-generation gating filter. Loading one "
            "fills the rule field only — your note is left untouched."
        ),
        "preset_overwrite_warning": (
            "The rule field already contains text. Click the button once "
            "more to replace it with the preset (your note is kept)."
        ),
        "gating_rule_label": "Select a gating-filter test rule",
        "load_gating_rule_btn": "🎯 Load the selected test rule",
        "gating_test_toast": (
            "🎯 Test rule loaded. Write your own thin note against it."
        ),
        "gating_test_caption": (
            "Choose a rule from the menu, then write YOUR OWN short, thin "
            "note against it — the goal is to provoke a 'gating' sentence "
            "(e.g. \"until X is confirmed, Y cannot be closed\") so you can "
            "check whether the filter actually rewrites it."
        ),
        "rule_label": "Triggered Rule / Alert",
        "note_label": "Investigator Note",
        "chars_caption": "{length} / {limit} characters",
        "analyze_btn": "Analyze the note",
        "reset_btn": "🧹 Clear input and result",
        "reset_help": (
            "Clears both input fields and the displayed result. Submits "
            "nothing and makes no API request."
        ),
        "reset_toast": "Input and result cleared.",
        "output_header": "### Assistant Analysis",
        "gating_checkbox": (
            "Apply experimental Gating Filter (Pre-test: 66.1% conversion)"
        ),
        "gating_help": (
            "Enables an experimental post-generation branch (pre-test "
            "screening only, non-confirmatory)."
        ),
        "empty_warning": (
            "Please fill in both fields: the rule/alert and the "
            "investigator note."
        ),
        "rule_too_long_warning": (
            "The \"Triggered Rule / Alert\" field is {length} characters "
            "against a limit of {limit}. Shorten the text yourself and try "
            "again — the app never truncates or summarizes your input for "
            "you. No API request was sent."
        ),
        "note_too_long_warning": (
            "The \"Investigator Note\" field is {length} characters against "
            "a limit of {limit}. Shorten the text yourself and try again — "
            "the app never truncates or summarizes your input for you. No "
            "API request was sent."
        ),
        "missing_key_warning": (
            "🔑 No Anthropic API key found. Analysis is disabled until you "
            "create `03 Demo/.streamlit/secrets.toml` with your own "
            "`ANTHROPIC_API_KEY` (see HOW_TO_RUN.md and the "
            "`secrets.toml.example` file). The key stays on your machine "
            "and is never displayed in the interface."
        ),
        "gating_info": (
            "🧪 Post-generation filter applied. The result comes from an "
            "experimental branch (66.1% conversion rate, pre-test, "
            "non-confirmatory) and is not part of the production logic."
        ),
        "reading_spinner": "The assistant is reading the note...",
        "base_expander": "Base response (before filter)",
        "base_available_caption": (
            "The base response remains available, unchanged, in the "
            "expander above."
        ),
        "err_auth": (
            "Authentication with the Anthropic API failed. Check the key in "
            "`.streamlit/secrets.toml` — it is likely invalid or expired. "
            "The request is not retried automatically."
        ),
        "err_rate_limit": (
            "The API rejected the request due to rate limiting. Wait a "
            "moment and try again."
        ),
        "err_timeout": (
            "The API request timed out. Try again; if it persists, check "
            "your connection."
        ),
        "err_connection": (
            "Could not reach the Anthropic API. Check your internet "
            "connection and try again."
        ),
        "err_invalid_request": (
            "The API rejected the request as invalid. Try shorter input; "
            "the request is not retried automatically."
        ),
        "err_provider": (
            "The API provider returned an error. Try again shortly."
        ),
        "filtered_header": "#### Filtered result (experimental)",
        "filter_spinner": "Applying the post-generation filter...",
        "filter_fallback": (
            "The filter could not be applied ({reason}) The base "
            "(unfiltered) response is shown instead."
        ),
        "integrity_error_title": (
            "🛑 Contract integrity check failed — the demo refuses to start "
            "with an unverified contract and carries no hardcoded fallback "
            "copy. Do not change the expected hash; see "
            "`02 Skill/.../reference/VERIFY.md`."
        ),
        "methodology_md": """
        ## 📖 About the Assistant (Methodology)

        ### 1. What is the assistant?

        This is an **advisory investigation-note quality assistant**, built
        to support analysts working in financial investigations (AML /
        anti-fraud). Its only job is to make a note **clearer, better
        supported and more defensible** before it is finalised — without
        ever taking over the human's role.

        The demo uses fully synthetic financial-investigation examples
        (including AML and anti-fraud contexts), but the product is **not
        an AML/compliance system**: it performs no transaction monitoring,
        no case management, no filing with authorities (e.g. SAR/STR), no
        policy enforcement, and makes no decisions for the user.

        The assistant explicitly does **NOT**:

        - decide whether activity is fraudulent, suspicious or legitimate;
        - make decisions about closure, escalation, restrictions or SAR/STR
          filing;
        - grade, rank, score, or assign a PASS/FAIL status;
        - state that a note is "ready", "approved" or "cleared";
        - invent facts, checks, relationships, dates, amounts or outcomes.

        The final decision always remains with the human analyst. Nothing in
        the assistant's output authorises submission, closure or escalation.

        ### 2. Methodology — a five-stage framework

        The assistant reads every note through an internal analytical lens:
        *trigger → context → checks → findings → rationale → action*.
        This is only an internal reading model — it is never imposed on the
        note as a required structure.

        **Stage 1 — Evidence-first reading.** Every observation is grounded
        in what the note shows or verifiably omits. Three distinct states
        are maintained and never collapsed: "shown" (it is recorded), "not
        shown" (the note says nothing either way) and "shown absent" (the
        note records that something did not happen). The single most
        consequential possible error — converting "not shown" into "was not
        done" — is explicitly prohibited, because absence of documentation
        is not evidence of absence of work. The assistant comments on the
        **documentation, never on the analyst's work** itself.

        **Stage 2 — Typology discipline.** A typology (e.g. structuring,
        layering, mule activity) is a name for a pattern, not a substitute
        for showing the pattern. The assistant may never import a typology
        on its own — neither as a hard assertion ("this is structuring") nor
        in a hedged form ("the amounts are consistent with structuring").
        The prohibition is **symmetrical**: exculpatory explanations the
        note does not carry ("this is probably routine settlement activity")
        are equally prohibited. The only exception: if **the note itself**
        names a typology, the assistant may and should test it against the
        facts the note itself shows.

        **Stage 3 — Decision ownership.** Decisions already taken
        (escalation, SAR/STR referral, restriction, termination) are
        human-owned and closed to the assistant. It may confirm that the
        decision is clearly stated and that its documented basis is
        internally coherent — including honestly noting that the basis is
        partial. It may not re-question the decision ("was escalation
        needed?"), endorse it, or propose alternative actions.

        **Stage 4 — Analyst-trust filter.** Before asking any question of
        the "how / with what / which specific" kind, the assistant
        classifies its target. Facts the analyst was positioned to verify
        in internal systems (a password, device or IP linkage; membership
        of a flagged group; a check performed in an internal tool;
        documentation received, or recorded as not received) are **trusted
        and not interrogated**. Conversely: load-bearing facts the analyst
        could not verify internally — an external party's intent, an
        explanation given by a counterparty — are not covered by trust and
        may be the subject of a focused question.

        **Stage 5 — Response gate.** Only **material gaps** are raised —
        gaps whose filling would change the conclusion or the action, not
        gaps that would merely make the note "tidier". On a benign no-action
        case (false positive) not a single "polish" suggestion is allowed;
        on a live escalated case — at most one. Stacking suggestions of
        declining relevance is prohibited. If there is no material gap, the
        assistant says so briefly, in natural prose, and stops.

        ### 3. Evidence base

        The contract was formally evaluated once, against a locked held-out
        set of **50 notes (n=50)**, marked by the domain owner against his
        own blind key — **not** "200 notes assessed by experts", as an
        earlier version of this text claimed. The result:

        - **Finding** (catching a real material gap): **50.0% (4/8)** —
          bar ≥60%, **missed**.
        - **Restraint** (share of the assistant's demands judged
          unnecessary): **55.2% (32/58)** — bar ≤25%, **missed**. That is,
          more than half of the assistant's points were superfluous —
          lower is better.

        Measured against the pinned contract body (hash
        `2f574a66…e58363`), model `claude-haiku-4-5`, temperature 1.0,
        n=50. **Both pre-registered bars were missed** — see `04 Evidence
        and Records/` for the full result and its conditions. Known
        defects were also recorded on the evaluated configuration —
        including one confirmed invention of an external fact (a wrong
        MCC category claim) — so check any code or typology claim before
        relying on it. This demo calls the same model, but it is a
        different, unevaluated harness (a different request shape, a
        streaming UI, no hash gate on every call, no one-note-per-call
        guarantee) — under the project's evidence label a new
        configuration starts with zero inherited evidence, so the figures
        above do not carry over to it.

        ### 4. The Gating Filter — an experimental post-generation control

        The gating filter is a second, extremely narrow prompt that runs
        **after** the main analysis is generated, and only when the checkbox
        in the Test Site is enabled.

        What it does:

        - **Catches aggressive conditional constructions** — sentences that
          tie a named documentation gap to a blocked or required consequence
          via precondition/sequencing language: "until…", "without…",
          "before…", "cannot…". Example: *"Until the link between the
          senders is documented, the escalation cannot be defended."*
        - **Rewrites them into purely descriptive form** — the gap is still
          named, but the blocking "precondition" wiring is dropped. Example
          after the filter: *"The note does not show what link was
          established between the senders."*
        - **Is instructed to change nothing else** — the filter's prompt
          requires it to rewrite only the targeted conditional
          constructions, leave every other sentence unchanged, and return
          the text verbatim if no such sentence exists. Because the
          filtered result is model-generated, exact preservation is **not
          mechanically guaranteed** — which is why the original base
          response always remains available separately and unchanged, for
          comparison. The text between the `<<<TEXT … TEXT>>>` markers is
          treated as inert data, never as instructions to the filter.

        ### 5. Custom mode — the rule is not evidence

        In Custom mode, the rule / alert context you supply defines **what
        the note needs to document**. The investigation note itself is
        **the evidence under review**. A condition that appears only in
        the rule must never be treated as proof that it actually occurred.
        Because model outputs may occasionally fail this separation,
        verify that every claimed fact is actually supported by the note.
        As everywhere in this demo — enter synthetic content only.
        """,
        "demo_vs_skill_md": """
        ### 6. What this demo is NOT

        The project has three separate distribution forms, and they are not
        interchangeable:

        - **The pinned contract** (`01 Contract/`) — the evaluated text,
          hash `2f574a66…e58363`.
        - **The Skill distribution** (`02 Skill/`) — packaged, but **never
          behaviourally tested in an actual host**; three of its eight
          acceptance-condition rows remain open or untested.
        - **This Streamlit demo** — a separate, unevaluated harness. It
          uses the same contract body (verified on every start), but
          inherits neither the n=50 result nor the Skill's status.

        The demo deliberately does **not** implement the Skill's session
        rules: no model self-declaration line, no one-case-per-session
        rule, no addressee sentence ("this feedback concerns the note, not
        its author"), no refusal flow for "so can I submit it?" follow-ups,
        and no heuristic real-data check. Those are rules of the Skill
        form; here they are documented, not implemented.
        """,
        "pretest_header": "##### Pre-test results",
        "metric1_label": "Pre-test conversion",
        "metric2_label": "Target",
        "metric3_label": "Status",
        "metric3_value": "Experimental",
        "pretest_md": """
        The **66.1% conversion** result (against a 70% target) is marked
        as promising but not yet sufficient. Measured on
        `claude-haiku-4-5`, temperature 0, prompt v0.3, as a **pre-test
        screening** run against 56 already-known "gating" responses from
        HMB-29 — **not** a confirmatory two-arm test, and the filter's
        status remains "promising, not adopted, not rejected." For that
        reason the filter is **deliberately not part of the
        application's production logic** — it is available only as an
        experimental option in the Test Site, and additional adversarial
        testing is required before any eventual integration.

        ---
        """,
        "synthetic_warning": (
            "**Important — synthetic data.** All scenarios, rules, alerts and "
            "notes in this application are 100% artificially created "
            "(fictional). They contain no real customer, banking or corporate "
            "information. The tool is strictly advisory and must not be used "
            "as the sole or final source when making decisions."
        ),
        "no_real_data": (
            "**Do not paste real data.** Never enter real investigation "
            "notes, customer data, account numbers, names, or internal "
            "rule/system name strings. Use only synthetic content — like "
            "the bundled scenarios."
        ),
        "footer_caption": "Built with Streamlit and the Anthropic API (Claude).",
    },
}
