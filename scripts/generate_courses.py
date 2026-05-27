#!/usr/bin/env python3
"""
Generate courses for Chinese speakers learning multiple languages.
Output goes to courses/zh-<lang>/ as YAML files.
"""
import os
import hashlib

COURSES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "courses")

# --- Course Definitions ---
# Each course: "course_id": { "name": ..., "code": ..., "for_speakers_of": ..., "special_chars": [...], modules: [...] }
# Each module: { "name": ..., skills: [...] }
# Each skill: { "name": ..., "id": N, words: [...], phrases: [...], mini_dictionary: {...} }
# Each word: { "word": ..., "translation": ..., "synonyms": [...], "images": [...] }

def hash_id(*parts):
    """Generate deterministic ID from parts"""
    raw = "|".join(parts)
    return hashlib.md5(raw.encode()).hexdigest()[:12]

def create_course_yaml(course_id, course_info):
    """Create a complete YAML course structure"""
    lang_name = course_info["name"]
    lang_code = course_info["code"]
    source_lang = course_info.get("for_speakers_of", "Chinese")
    source_code = "zh"
    
    # Build skill YAMLs
    modules = course_info["modules"]
    skill_files_by_module = []
    
    for mod in modules:
        mod_name = mod["name"]
        mod_dirname = mod_name.lower().replace(" ", "-")
        skill_filenames = []
        
        os.makedirs(f"{COURSES_DIR}/{course_id}/{mod_dirname}/skills", exist_ok=True)
        
        for skill_idx, skill in enumerate(mod["skills"]):
            skill_name = skill["name"]
            skill_id = skill_idx + 1
            skill_filename = f"{skill_name.lower().replace(' ', '-').replace('(', '').replace(')', '')}.yaml"
            skill_filenames.append(skill_filename)
            
            # Build mini-dictionary
            mini_dict = {}
            if "mini_dictionary" in skill:
                mini_dict = skill["mini_dictionary"]
            else:
                mini_dict = {lang_name: [], "Chinese": []}
                # Add words to dictionary
                for w in skill["words"]:
                    mini_dict.setdefault(lang_name, []).append(f"{w['word']}: {w.get('definition_note', w['translation'])}")
                    mini_dict.setdefault("Chinese", []).append(f"{w['translation']}: {w['word']}")
                # Clean duplicates
                for k in mini_dict:
                    mini_dict[k] = list(set(mini_dict[k]))
            
            # Generate YAML content
            special_chars_str = ""
            if "special_chars" in skill:
                sc_list = "\n".join([f'    - "{c}"' for c in skill["special_chars"]])
                special_chars_str = f"\n  Special characters:\n{sc_list}"
            
            # Images for words
            words_yaml = []
            for w in skill["words"]:
                word_yaml = f"""  - Word: {w['word']}
    Translation: {w['translation']}"""
                if w.get("synonyms"):
                    syns = "\n".join([f'      - "{s}"' for s in w["synonyms"]])
                    word_yaml += f"""
    Synonyms:
{syns}"""
                if w.get("also_accepted"):
                    acc = "\n".join([f'      - "{a}"' for a in w["also_accepted"]])
                    word_yaml += f"""
    Also accepted:
{acc}"""
                if w.get("images"):
                    imgs = "\n".join([f'      - {img}' for img in w["images"]])
                    word_yaml += f"""
    Images:
{imgs}"""
                words_yaml.append(word_yaml)
            
            # Phrases
            phrases_yaml = []
            for p in skill.get("phrases", []):
                phrase_yaml = f"""  - Phrase: {p['phrase']}
    Translation: {p['translation']}"""
                if p.get("alternative_versions"):
                    alts = "\n".join([f'      - {a}' for a in p["alternative_versions"]])
                    phrase_yaml += f"""
    Alternative versions:
{alts}"""
                phrases_yaml.append(phrase_yaml)
            
            # Mini-dictionary
            mini_dict_sections = []
            for lang, entries in mini_dict.items():
                entries_yaml = "\n".join([f'    - {e}' for e in entries])
                mini_dict_sections.append(f"""  {lang}:
{entries_yaml}""")
            
            skill_yaml = f"""Skill:
  Name: {skill_name}
  Id: {skill_id}
  Thumbnails:
    - thumbnail1
    - thumbnail2
    - thumbnail3
  {special_chars_str}

New words:
{chr(10).join(words_yaml)}

Phrases:
{chr(10).join(phrases_yaml)}

Mini-dictionary:
{chr(10).join(mini_dict_sections)}
"""
            
            with open(f"{COURSES_DIR}/{course_id}/{mod_dirname}/skills/{skill_filename}", "w", encoding="utf-8") as f:
                f.write(skill_yaml)
        
        # Module YAML
        skill_refs = "\n".join([f'  - {f}' for f in skill_filenames])
        module_yaml = f"""Module:
  Name: "{mod_name}"

Skills:
{skill_refs}
"""
        with open(f"{COURSES_DIR}/{course_id}/{mod_dirname}/module.yaml", "w", encoding="utf-8") as f:
            f.write(module_yaml)
        
        skill_files_by_module.append((mod_dirname, skill_filenames))
    
    # Course YAML
    special_chars = course_info.get("special_chars", [])
    sc_list = "\n".join([f'  - "{c}"' for c in special_chars])
    module_refs = "\n".join([f'  - {m}' for m, _ in skill_files_by_module])
    
    course_yaml = f"""Course:
  Language:
    Name: {lang_name}
    IETF BCP 47: {lang_code}

  For speakers of:
    Name: {source_lang}
    IETF BCP 47: {source_code}

  License:
    Name: Attribution-ShareAlike 4.0 International
    Short name: CC BY-SA 4.0
    Link: https://creativecommons.org/licenses/by-sa/4.0/legalcode

  Repository: https://github.com/xixil136136-ui/LibreLingo

  Special characters:
{sc_list}

Modules:
{module_refs}

Settings:
    Audio:
      Enabled: True
"""
    with open(f"{COURSES_DIR}/{course_id}/course.yaml", "w", encoding="utf-8") as f:
        f.write(course_yaml)

def define_courses():
    """Define all courses"""
    
    zh_en = {
        "name": "English",
        "code": "en",
        "for_speakers_of": "Chinese",
        "special_chars": ["'", "é", "á", "í", "ó", "ú", "ü"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "hello", "translation": "你好"},
                            {"word": "goodbye", "translation": "再见"},
                            {"word": "good morning", "translation": "早上好"},
                            {"word": "good evening", "translation": "晚上好"},
                            {"word": "how are you", "translation": "你好吗"},
                            {"word": "I'm fine", "translation": "我很好"},
                            {"word": "please", "translation": "请"},
                            {"word": "thank you", "translation": "谢谢"},
                            {"word": "you're welcome", "translation": "不客气"},
                            {"word": "sorry", "translation": "对不起"},
                        ],
                        "phrases": [
                            {"phrase": "Hello, how are you?", "translation": "你好，你好吗？"},
                            {"phrase": "Good morning, thank you.", "translation": "早上好，谢谢。"},
                            {"phrase": "I'm fine, thank you.", "translation": "我很好，谢谢。"},
                            {"phrase": "Goodbye, see you later.", "translation": "再见，回头见。"},
                            {"phrase": "Please, come in.", "translation": "请进。"},
                        ],
                        "mini_dictionary": {
                            "English": [
                                "hello: 你好",
                                "goodbye: 再见",
                                "good morning: 早上好",
                                "good evening: 晚上好",
                                "how are you: 你好吗",
                                "I'm fine: 我很好",
                                "please: 请",
                                "thank you: 谢谢",
                                "you're welcome: 不客气",
                                "sorry: 对不起",
                                "see you later: 回头见",
                                "come in: 进来",
                            ],
                            "Chinese": [
                                "你好: hello",
                                "再见: goodbye",
                                "早上好: good morning",
                                "晚上好: good evening",
                                "你好吗: how are you",
                                "我很好: I'm fine",
                                "请: please",
                                "谢谢: thank you",
                                "不客气: you're welcome",
                                "对不起: sorry",
                                "回头见: see you later",
                                "进来: come in",
                            ],
                        },
                    },
                    {
                        "name": "Numbers",
                        "special_chars": [],
                        "words": [
                            {"word": "one", "translation": "一"},
                            {"word": "two", "translation": "二"},
                            {"word": "three", "translation": "三"},
                            {"word": "four", "translation": "四"},
                            {"word": "five", "translation": "五"},
                            {"word": "six", "translation": "六"},
                            {"word": "seven", "translation": "七"},
                            {"word": "eight", "translation": "八"},
                            {"word": "nine", "translation": "九"},
                            {"word": "ten", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "One, two, three.", "translation": "一、二、三。"},
                            {"phrase": "Four and five.", "translation": "四和五。"},
                            {"phrase": "Six, seven, eight.", "translation": "六、七、八。"},
                            {"phrase": "Nine and ten.", "translation": "九和十。"},
                            {"phrase": "It's five o'clock.", "translation": "现在五点钟。"},
                        ],
                        "mini_dictionary": {
                            "English": [
                                "one: 一",
                                "two: 二",
                                "three: 三",
                                "four: 四",
                                "five: 五",
                                "six: 六",
                                "seven: 七",
                                "eight: 八",
                                "nine: 九",
                                "ten: 十",
                                "o'clock: 点钟",
                                "and: 和",
                            ],
                            "Chinese": [
                                "一: one",
                                "二: two",
                                "三: three",
                                "四: four",
                                "五: five",
                                "六: six",
                                "七: seven",
                                "八: eight",
                                "九: nine",
                                "十: ten",
                                "点钟: o'clock",
                                "和: and",
                            ],
                        },
                    },
                ],
            },
            {
                "name": "Food & Drink",
                "skills": [
                    {
                        "name": "Basic Foods",
                        "special_chars": [],
                        "words": [
                            {"word": "water", "translation": "水"},
                            {"word": "bread", "translation": "面包"},
                            {"word": "rice", "translation": "米饭"},
                            {"word": "milk", "translation": "牛奶"},
                            {"word": "egg", "translation": "鸡蛋"},
                            {"word": "chicken", "translation": "鸡肉"},
                            {"word": "fish", "translation": "鱼"},
                            {"word": "fruit", "translation": "水果"},
                            {"word": "vegetable", "translation": "蔬菜"},
                            {"word": "tea", "translation": "茶"},
                            {"word": "coffee", "translation": "咖啡"},
                            {"word": "sugar", "translation": "糖"},
                        ],
                        "phrases": [
                            {"phrase": "I want water.", "translation": "我想要水。"},
                            {"phrase": "Bread and milk, please.", "translation": "请给我面包和牛奶。"},
                            {"phrase": "I like rice.", "translation": "我喜欢米饭。"},
                            {"phrase": "Tea or coffee?", "translation": "茶还是咖啡？"},
                            {"phrase": "This is delicious.", "translation": "这个很好吃。"},
                        ],
                    },
                    {
                        "name": "Restaurant",
                        "special_chars": [],
                        "words": [
                            {"word": "menu", "translation": "菜单"},
                            {"word": "waiter", "translation": "服务员"},
                            {"word": "bill", "translation": "账单"},
                            {"word": "table", "translation": "桌子"},
                            {"word": "fork", "translation": "叉子"},
                            {"word": "knife", "translation": "刀"},
                            {"word": "spoon", "translation": "勺子"},
                            {"word": "plate", "translation": "盘子"},
                            {"word": "cup", "translation": "杯子"},
                            {"word": "tip", "translation": "小费"},
                        ],
                        "phrases": [
                            {"phrase": "Can I see the menu?", "translation": "我能看看菜单吗？"},
                            {"phrase": "I'd like to order.", "translation": "我想点餐。"},
                            {"phrase": "The bill, please.", "translation": "请给我账单。"},
                            {"phrase": "A table for two.", "translation": "两个人的桌子。"},
                            {"phrase": "This is very good.", "translation": "这个非常好。"},
                        ],
                    },
                ],
            },
            {
                "name": "Travel",
                "skills": [
                    {
                        "name": "Directions",
                        "special_chars": [],
                        "words": [
                            {"word": "left", "translation": "左边"},
                            {"word": "right", "translation": "右边"},
                            {"word": "straight", "translation": "直走"},
                            {"word": "here", "translation": "这里"},
                            {"word": "there", "translation": "那里"},
                            {"word": "near", "translation": "附近"},
                            {"word": "far", "translation": "远"},
                            {"word": "map", "translation": "地图"},
                            {"word": "street", "translation": "街道"},
                            {"word": "road", "translation": "路"},
                        ],
                        "phrases": [
                            {"phrase": "Where is the station?", "translation": "车站在哪里？"},
                            {"phrase": "Turn left here.", "translation": "在这里左转。"},
                            {"phrase": "Go straight ahead.", "translation": "一直往前走。"},
                            {"phrase": "Is it far from here?", "translation": "离这里远吗？"},
                            {"phrase": "I need a map.", "translation": "我需要一张地图。"},
                        ],
                    },
                    {
                        "name": "Transportation",
                        "special_chars": [],
                        "words": [
                            {"word": "airport", "translation": "机场"},
                            {"word": "train", "translation": "火车"},
                            {"word": "bus", "translation": "公共汽车"},
                            {"word": "taxi", "translation": "出租车"},
                            {"word": "subway", "translation": "地铁"},
                            {"word": "ticket", "translation": "票"},
                            {"word": "passport", "translation": "护照"},
                            {"word": "hotel", "translation": "酒店"},
                            {"word": "luggage", "translation": "行李"},
                            {"word": "platform", "translation": "站台"},
                        ],
                        "phrases": [
                            {"phrase": "Where is the airport?", "translation": "机场在哪里？"},
                            {"phrase": "I need a taxi.", "translation": "我需要一辆出租车。"},
                            {"phrase": "How much is the ticket?", "translation": "这张票多少钱？"},
                            {"phrase": "The train is late.", "translation": "火车晚点了。"},
                            {"phrase": "I have a reservation.", "translation": "我有预约。"},
                        ],
                    },
                ],
            },
            {
                "name": "Daily Life",
                "skills": [
                    {
                        "name": "Shopping",
                        "special_chars": [],
                        "words": [
                            {"word": "shop", "translation": "商店"},
                            {"word": "price", "translation": "价格"},
                            {"word": "expensive", "translation": "贵的"},
                            {"word": "cheap", "translation": "便宜的"},
                            {"word": "money", "translation": "钱"},
                            {"word": "discount", "translation": "折扣"},
                            {"word": "size", "translation": "尺寸"},
                            {"word": "color", "translation": "颜色"},
                            {"word": "try on", "translation": "试穿"},
                            {"word": "receipt", "translation": "收据"},
                        ],
                        "phrases": [
                            {"phrase": "How much is this?", "translation": "这个多少钱？"},
                            {"phrase": "It's too expensive.", "translation": "太贵了。"},
                            {"phrase": "Do you have a discount?", "translation": "有折扣吗？"},
                            {"phrase": "Can I try this on?", "translation": "我能试穿这个吗？"},
                            {"phrase": "I'll take it.", "translation": "我买了。"},
                        ],
                    },
                    {
                        "name": "Weather",
                        "special_chars": [],
                        "words": [
                            {"word": "sunny", "translation": "晴天"},
                            {"word": "rain", "translation": "雨"},
                            {"word": "snow", "translation": "雪"},
                            {"word": "wind", "translation": "风"},
                            {"word": "cloud", "translation": "云"},
                            {"word": "cold", "translation": "冷"},
                            {"word": "hot", "translation": "热"},
                            {"word": "warm", "translation": "温暖"},
                            {"word": "temperature", "translation": "温度"},
                            {"word": "umbrella", "translation": "雨伞"},
                        ],
                        "phrases": [
                            {"phrase": "It's sunny today.", "translation": "今天天气晴朗。"},
                            {"phrase": "It's going to rain.", "translation": "要下雨了。"},
                            {"phrase": "It's very cold outside.", "translation": "外面很冷。"},
                            {"phrase": "What's the temperature?", "translation": "多少度？"},
                            {"phrase": "Bring an umbrella.", "translation": "带上雨伞。"},
                        ],
                    },
                ],
            },
        ],
    }
    
    zh_ja = {
        "name": "Japanese",
        "code": "ja",
        "for_speakers_of": "Chinese",
        "special_chars": ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ", "さ", "し", "す", "せ", "そ"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "こんにちは", "translation": "你好"},
                            {"word": "さようなら", "translation": "再见"},
                            {"word": "おはようございます", "translation": "早上好"},
                            {"word": "こんばんは", "translation": "晚上好"},
                            {"word": "ありがとう", "translation": "谢谢"},
                            {"word": "すみません", "translation": "对不起/不好意思"},
                            {"word": "はい", "translation": "是的"},
                            {"word": "いいえ", "translation": "不是"},
                            {"word": "お願いします", "translation": "请"},
                            {"word": "大丈夫", "translation": "没关系"},
                        ],
                        "phrases": [
                            {"phrase": "こんにちは、元気ですか？", "translation": "你好，你好吗？"},
                            {"phrase": "ありがとうございます。", "translation": "非常感谢。"},
                            {"phrase": "すみません、ちょっと待ってください。", "translation": "对不起，请稍等。"},
                            {"phrase": "おはようございます、先生。", "translation": "早上好，老师。"},
                            {"phrase": "さようなら、また会いましょう。", "translation": "再见，后会有期。"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": [],
                        "words": [
                            {"word": "一", "translation": "一（いち）"},
                            {"word": "二", "translation": "二（に）"},
                            {"word": "三", "translation": "三（さん）"},
                            {"word": "四", "translation": "四（し/よん）"},
                            {"word": "五", "translation": "五（ご）"},
                            {"word": "六", "translation": "六（ろく）"},
                            {"word": "七", "translation": "七（しち/なな）"},
                            {"word": "八", "translation": "八（はち）"},
                            {"word": "九", "translation": "九（く/きゅう）"},
                            {"word": "十", "translation": "十（じゅう）"},
                        ],
                        "phrases": [
                            {"phrase": "一、二、三。", "translation": "一、二、三。"},
                            {"phrase": "五時です。", "translation": "现在五点钟。"},
                            {"phrase": "十人います。", "translation": "有十个人。"},
                        ],
                    },
                ],
            },
            {
                "name": "Food & Drink",
                "skills": [
                    {
                        "name": "Basic Foods",
                        "special_chars": [],
                        "words": [
                            {"word": "水", "translation": "水"},
                            {"word": "ご飯", "translation": "米饭"},
                            {"word": "パン", "translation": "面包"},
                            {"word": "牛乳", "translation": "牛奶"},
                            {"word": "卵", "translation": "鸡蛋"},
                            {"word": "魚", "translation": "鱼"},
                            {"word": "肉", "translation": "肉"},
                            {"word": "野菜", "translation": "蔬菜"},
                            {"word": "果物", "translation": "水果"},
                            {"word": "お茶", "translation": "茶"},
                            {"word": "コーヒー", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "水をください。", "translation": "请给我水。"},
                            {"phrase": "ご飯を食べます。", "translation": "吃饭。"},
                            {"phrase": "お茶が好きです。", "translation": "我喜欢喝茶。"},
                            {"phrase": "美味しいですね。", "translation": "很好吃呢。"},
                        ],
                    },
                ],
            },
        ],
    }
    
    zh_ko = {
        "name": "Korean",
        "code": "ko",
        "for_speakers_of": "Chinese",
        "special_chars": ["가", "나", "다", "라", "마", "바", "사", "아", "자", "차"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "안녕하세요", "translation": "你好"},
                            {"word": "안녕히 계세요", "translation": "再见"},
                            {"word": "감사합니다", "translation": "谢谢"},
                            {"word": "죄송합니다", "translation": "对不起"},
                            {"word": "네", "translation": "是的"},
                            {"word": "아니요", "translation": "不是"},
                            {"word": "괜찮습니다", "translation": "没关系"},
                            {"word": "잠시만요", "translation": "请稍等"},
                            {"word": "주세요", "translation": "请给我"},
                            {"word": "만나서 반갑습니다", "translation": "很高兴认识你"},
                        ],
                        "phrases": [
                            {"phrase": "안녕하세요, 반갑습니다.", "translation": "你好，很高兴认识你。"},
                            {"phrase": "감사합니다, 선생님.", "translation": "谢谢您，老师。"},
                            {"phrase": "죄송합니다, 늦었습니다.", "translation": "对不起，我迟到了。"},
                            {"phrase": "네, 괜찮습니다.", "translation": "是的，没关系。"},
                            {"phrase": "안녕히 계세요, 또 만나요.", "translation": "再见，下次见。"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": [],
                        "words": [
                            {"word": "일", "translation": "一"},
                            {"word": "이", "translation": "二"},
                            {"word": "삼", "translation": "三"},
                            {"word": "사", "translation": "四"},
                            {"word": "오", "translation": "五"},
                            {"word": "육", "translation": "六"},
                            {"word": "칠", "translation": "七"},
                            {"word": "팔", "translation": "八"},
                            {"word": "구", "translation": "九"},
                            {"word": "십", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "일, 이, 삼.", "translation": "一、二、三。"},
                            {"phrase": "지금 다섯 시입니다.", "translation": "现在五点钟。"},
                            {"phrase": "열 명이 있습니다.", "translation": "有十个人。"},
                        ],
                    },
                ],
            },
            {
                "name": "Food & Drink",
                "skills": [
                    {
                        "name": "Basic Foods",
                        "special_chars": [],
                        "words": [
                            {"word": "물", "translation": "水"},
                            {"word": "밥", "translation": "米饭"},
                            {"word": "빵", "translation": "面包"},
                            {"word": "우유", "translation": "牛奶"},
                            {"word": "계란", "translation": "鸡蛋"},
                            {"word": "생선", "translation": "鱼"},
                            {"word": "고기", "translation": "肉"},
                            {"word": "야채", "translation": "蔬菜"},
                            {"word": "과일", "translation": "水果"},
                            {"word": "차", "translation": "茶"},
                            {"word": "커피", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "물 주세요.", "translation": "请给我水。"},
                            {"phrase": "밥을 먹습니다.", "translation": "吃饭。"},
                            {"phrase": "차가 좋아요.", "translation": "我喜欢茶。"},
                            {"phrase": "맛있습니다.", "translation": "很好吃。"},
                        ],
                    },
                ],
            },
        ],
    }
    
    zh_fr = {
        "name": "French",
        "code": "fr",
        "for_speakers_of": "Chinese",
        "special_chars": ["é", "è", "ê", "ë", "à", "â", "î", "ï", "ô", "ù", "ç"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "bonjour", "translation": "你好/早上好"},
                            {"word": "bonsoir", "translation": "晚上好"},
                            {"word": "au revoir", "translation": "再见"},
                            {"word": "merci", "translation": "谢谢"},
                            {"word": "s'il vous plaît", "translation": "请"},
                            {"word": "pardon", "translation": "对不起"},
                            {"word": "oui", "translation": "是的"},
                            {"word": "non", "translation": "不是"},
                            {"word": "de rien", "translation": "不客气"},
                            {"word": "bonne journée", "translation": "祝好"},
                        ],
                        "phrases": [
                            {"phrase": "Bonjour, comment allez-vous ?", "translation": "你好，您好吗？"},
                            {"phrase": "Merci beaucoup.", "translation": "非常感谢。"},
                            {"phrase": "Au revoir, à demain.", "translation": "再见，明天见。"},
                            {"phrase": "Pardon, je suis en retard.", "translation": "对不起，我迟到了。"},
                            {"phrase": "De rien, bonne journée !", "translation": "不客气，祝好！"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": [],
                        "words": [
                            {"word": "un", "translation": "一"},
                            {"word": "deux", "translation": "二"},
                            {"word": "trois", "translation": "三"},
                            {"word": "quatre", "translation": "四"},
                            {"word": "cinq", "translation": "五"},
                            {"word": "six", "translation": "六"},
                            {"word": "sept", "translation": "七"},
                            {"word": "huit", "translation": "八"},
                            {"word": "neuf", "translation": "九"},
                            {"word": "dix", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "Un, deux, trois.", "translation": "一、二、三。"},
                            {"phrase": "Il est cinq heures.", "translation": "现在五点钟。"},
                            {"phrase": "Il y a dix personnes.", "translation": "有十个人。"},
                        ],
                    },
                ],
            },
            {
                "name": "Food & Drink",
                "skills": [
                    {
                        "name": "Basic Foods",
                        "special_chars": [],
                        "words": [
                            {"word": "eau", "translation": "水"},
                            {"word": "pain", "translation": "面包"},
                            {"word": "riz", "translation": "米饭"},
                            {"word": "lait", "translation": "牛奶"},
                            {"word": "œuf", "translation": "鸡蛋"},
                            {"word": "poulet", "translation": "鸡肉"},
                            {"word": "poisson", "translation": "鱼"},
                            {"word": "légume", "translation": "蔬菜"},
                            {"word": "fruit", "translation": "水果"},
                            {"word": "thé", "translation": "茶"},
                            {"word": "café", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "Je voudrais de l'eau.", "translation": "我想要水。"},
                            {"phrase": "Du pain et du lait, s'il vous plaît.", "translation": "请给我面包和牛奶。"},
                            {"phrase": "J'aime le riz.", "translation": "我喜欢米饭。"},
                            {"phrase": "C'est délicieux.", "translation": "这个很好吃。"},
                        ],
                    },
                ],
            },
        ],
    }
    
    return {
        "zh-en": zh_en,
        "zh-ja": zh_ja,
        "zh-ko": zh_ko,
        "zh-fr": zh_fr,
    }


def main():
    courses = define_courses()
    
    for course_id, course_info in courses.items():
        print(f"Generating course: {course_id} ({course_info['name']})")
        os.makedirs(f"{COURSES_DIR}/{course_id}", exist_ok=True)
        create_course_yaml(course_id, course_info)
        print(f"  Done: {course_id}")
    
    print("\nAll courses generated successfully!")
    print(f"\nCourse directories created:")
    for cid in courses:
        print(f"  courses/{cid}/")


if __name__ == "__main__":
    main()
