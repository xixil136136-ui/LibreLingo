#!/usr/bin/env python3
"""
Generate courses for Chinese speakers learning multiple languages.
Includes conversation/dialogue modules for real-world practice.
"""
import os
import hashlib

COURSES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "courses")


def hash_id(*parts):
    raw = "|".join(parts)
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def create_course_yaml(course_id, course_info):
    lang_name = course_info["name"]
    lang_code = course_info["code"]
    source_lang = course_info.get("for_speakers_of", "Chinese")
    source_code = "zh"

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

            mini_dict = {}
            if "mini_dictionary" in skill:
                mini_dict = skill["mini_dictionary"]
            else:
                mini_dict = {lang_name: [], "Chinese": []}
                for w in skill["words"]:
                    mini_dict.setdefault(lang_name, []).append(f"{w['word']}: {w.get('definition_note', w['translation'])}")
                    mini_dict.setdefault("Chinese", []).append(f"{w['translation']}: {w['word']}")
                for k in mini_dict:
                    mini_dict[k] = list(set(mini_dict[k]))

            special_chars_str = ""
            if "special_chars" in skill:
                sc_list = "\n".join([f'    - "{c}"' for c in skill["special_chars"]])
                special_chars_str = f"\n  Special characters:\n{sc_list}"

            words_yaml = []
            for w in skill["words"]:
                word_yaml = f"""  - Word: {w['word']}
    Translation: {w['translation']}"""
                if w.get("synonyms"):
                    syns = "\n".join([f'      - "{s}"' for s in w["synonyms"]])
                    word_yaml += f"""\n    Synonyms:\n{syns}"""
                if w.get("also_accepted"):
                    acc = "\n".join([f'      - "{a}"' for a in w["also_accepted"]])
                    word_yaml += f"""\n    Also accepted:\n{acc}"""
                if w.get("images"):
                    imgs = "\n".join([f'      - {img}' for img in w["images"]])
                    word_yaml += f"""\n    Images:\n{imgs}"""
                words_yaml.append(word_yaml)

            phrases_yaml = []
            for p in skill.get("phrases", []):
                phrase_yaml = f"""  - Phrase: {p['phrase']}
    Translation: {p['translation']}"""
                if p.get("alternative_versions"):
                    alts = "\n".join([f'      - {a}' for a in p["alternative_versions"]])
                    phrase_yaml += f"""\n    Alternative versions:\n{alts}"""
                phrases_yaml.append(phrase_yaml)

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

        skill_refs = "\n".join([f'  - {f}' for f in skill_filenames])
        module_yaml = f"""Module:
  Name: "{mod_name}"

Skills:
{skill_refs}
"""
        with open(f"{COURSES_DIR}/{course_id}/{mod_dirname}/module.yaml", "w", encoding="utf-8") as f:
            f.write(module_yaml)

        skill_files_by_module.append((mod_dirname, skill_filenames))

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


# ── Shared conversation module (added to EVERY course) ──────────────────────

def conversation_skills(lang_name, lang_label="en"):
    """Return a conversations module with real dialogue phrases.
    lang_name = target language name (e.g., 'German')
    lang_label = short label for dictionary (e.g., 'German')
    Returns list of skill dicts.
    """
    # Base conversations - these will be translated per language
    conv_base = {
        "en": {
            "restaurant": {
                "words": [
                    {"word": "I would like", "translation": "我想要"},
                    {"word": "menu", "translation": "菜单"},
                    {"word": "order", "translation": "点餐"},
                    {"word": "bill", "translation": "账单"},
                    {"word": "delicious", "translation": "美味"},
                    {"word": "recommendation", "translation": "推荐"},
                    {"word": "reservation", "translation": "预约"},
                    {"word": "waiter", "translation": "服务员"},
                    {"word": "table for two", "translation": "两人桌"},
                    {"word": "today's special", "translation": "今日特价"},
                ],
                "phrases": [
                    {"phrase": "I'd like to make a reservation.", "translation": "我想预约。"},
                    {"phrase": "A table for two, please.", "translation": "请给我一个两人桌。"},
                    {"phrase": "Can I see the menu?", "translation": "我能看看菜单吗？"},
                    {"phrase": "What do you recommend?", "translation": "你推荐什么？"},
                    {"phrase": "I'll have the steak, please.", "translation": "我要牛排。"},
                    {"phrase": "Could I have the bill, please?", "translation": "请给我账单。"},
                    {"phrase": "The food is delicious!", "translation": "食物太好吃了！"},
                    {"phrase": "Can I have some water?", "translation": "能给我一些水吗？"},
                    {"phrase": "Is service charge included?", "translation": "服务费包含在内吗？"},
                    {"phrase": "I'm allergic to peanuts.", "translation": "我对花生过敏。"},
                ],
            },
            "shopping": {
                "words": [
                    {"word": "How much", "translation": "多少钱"},
                    {"word": "discount", "translation": "折扣"},
                    {"word": "credit card", "translation": "信用卡"},
                    {"word": "cash", "translation": "现金"},
                    {"word": "size", "translation": "尺寸"},
                    {"word": "color", "translation": "颜色"},
                    {"word": "try on", "translation": "试穿"},
                    {"word": "receipt", "translation": "收据"},
                    {"word": "too expensive", "translation": "太贵"},
                    {"word": "exchange", "translation": "换货"},
                ],
                "phrases": [
                    {"phrase": "How much does this cost?", "translation": "这个多少钱？"},
                    {"phrase": "Can I try this on?", "translation": "我能试穿这个吗？"},
                    {"phrase": "Do you have this in a different color?", "translation": "有别的颜色吗？"},
                    {"phrase": "It's too expensive. Is there a discount?", "translation": "太贵了。有折扣吗？"},
                    {"phrase": "I'll take it. Can I pay by card?", "translation": "我买了。能用卡支付吗？"},
                    {"phrase": "Can I have a receipt, please?", "translation": "请给我收据。"},
                    {"phrase": "I'd like to exchange this.", "translation": "我想换这个。"},
                    {"phrase": "Do you have a smaller size?", "translation": "有小一点的尺寸吗？"},
                    {"phrase": "Is there a sale going on?", "translation": "有打折活动吗？"},
                    {"phrase": "I'm just looking, thanks.", "translation": "我就看看，谢谢。"},
                ],
            },
            "travel": {
                "words": [
                    {"word": "airport", "translation": "机场"},
                    {"word": "ticket", "translation": "票"},
                    {"word": "platform", "translation": "站台"},
                    {"word": "departure", "translation": "出发"},
                    {"word": "arrival", "translation": "到达"},
                    {"word": "one-way", "translation": "单程"},
                    {"word": "round trip", "translation": "往返"},
                    {"word": "passport", "translation": "护照"},
                    {"word": "visa", "translation": "签证"},
                    {"word": "customs", "translation": "海关"},
                ],
                "phrases": [
                    {"phrase": "Where is the airport?", "translation": "机场在哪里？"},
                    {"phrase": "I need a ticket to Berlin.", "translation": "我需要一张去柏林的票。"},
                    {"phrase": "One-way or round trip?", "translation": "单程还是往返？"},
                    {"phrase": "Which platform does the train leave from?", "translation": "火车从哪个站台出发？"},
                    {"phrase": "What time is the next bus?", "translation": "下一班车几点？"},
                    {"phrase": "Is this seat taken?", "translation": "这个座位有人吗？"},
                    {"phrase": "Can I see your passport, please?", "translation": "请出示您的护照。"},
                    {"phrase": "I have nothing to declare.", "translation": "我没有需要申报的物品。"},
                    {"phrase": "How long is the journey?", "translation": "旅途有多久？"},
                    {"phrase": "Please let me off at the next stop.", "translation": "请在下一站让我下车。"},
                ],
            },
            "hotel": {
                "words": [
                    {"word": "check in", "translation": "入住"},
                    {"word": "check out", "translation": "退房"},
                    {"word": "room key", "translation": "房卡"},
                    {"word": "single room", "translation": "单人间"},
                    {"word": "double room", "translation": "双人间"},
                    {"word": "reservation", "translation": "预订"},
                    {"word": "breakfast", "translation": "早餐"},
                    {"word": "WiFi", "translation": "无线网络"},
                    {"word": "air conditioning", "translation": "空调"},
                    {"word": "room service", "translation": "客房服务"},
                ],
                "phrases": [
                    {"phrase": "I have a reservation.", "translation": "我有预订。"},
                    {"phrase": "I'd like to check in, please.", "translation": "我想办理入住。"},
                    {"phrase": "How much is a double room per night?", "translation": "双人间一晚多少钱？"},
                    {"phrase": "Is breakfast included?", "translation": "包含早餐吗？"},
                    {"phrase": "What's the WiFi password?", "translation": "WiFi密码是什么？"},
                    {"phrase": "The air conditioning isn't working.", "translation": "空调坏了。"},
                    {"phrase": "Can I have a wake-up call at 7am?", "translation": "能给我设置早上7点的叫醒服务吗？"},
                    {"phrase": "I'd like to check out, please.", "translation": "我想退房。"},
                    {"phrase": "Can I store my luggage here?", "translation": "我能寄存行李吗？"},
                    {"phrase": "Thank you for a wonderful stay!", "translation": "谢谢，住得很愉快！"},
                ],
            },
        }
    }

    # ── Language-specific translations ──

    def t(target, translations):
        """Get the translation for this specific language"""
        return translations.get(lang_label, translations.get("en", target))

    # German translations
    de = {
        "我想要": "Ich möchte",
        "菜单": "die Speisekarte",
        "点餐": "bestellen",
        "账单": "die Rechnung",
        "美味": "köstlich",
        "推荐": "die Empfehlung",
        "预约": "die Reservierung",
        "服务员": "der Kellner",
        "两人桌": "ein Tisch für zwei",
        "今日特价": "das Tagesgericht",
        "我想预约。": "Ich möchte eine Reservierung vornehmen.",
        "请给我一个两人桌。": "Einen Tisch für zwei, bitte.",
        "我能看看菜单吗？": "Kann ich die Speisekarte sehen?",
        "你推荐什么？": "Was empfehlen Sie?",
        "我要牛排。": "Ich nehme das Steak.",
        "请给我账单。": "Kann ich bitte die Rechnung haben?",
        "食物太好吃了！": "Das Essen ist köstlich!",
        "能给我一些水吗？": "Kann ich etwas Wasser haben?",
        "服务费包含在内吗？": "Ist die Bedienung inklusive?",
        "我对花生过敏。": "Ich bin allergisch gegen Erdnüsse.",
        # shopping
        "多少钱": "Wie viel",
        "折扣": "der Rabatt",
        "信用卡": "die Kreditkarte",
        "现金": "das Bargeld",
        "尺寸": "die Größe",
        "颜色": "die Farbe",
        "试穿": "anprobieren",
        "收据": "die Quittung",
        "太贵": "zu teuer",
        "换货": "umtauschen",
        "这个多少钱？": "Wie viel kostet das?",
        "我能试穿这个吗？": "Kann ich das anprobieren?",
        "有别的颜色吗？": "Haben Sie das in einer anderen Farbe?",
        "太贵了。有折扣吗？": "Das ist zu teuer. Gibt es einen Rabatt?",
        "我买了。能用卡支付吗？": "Ich nehme es. Kann ich mit Karte bezahlen?",
        "请给我收据。": "Kann ich bitte eine Quittung haben?",
        "我想换这个。": "Ich möchte das umtauschen.",
        "有小一点的尺寸吗？": "Haben Sie eine kleinere Größe?",
        "有打折活动吗？": "Gibt es einen Ausverkauf?",
        "我就看看，谢谢。": "Ich schaue nur, danke.",
        # travel
        "机场": "der Flughafen",
        "票": "die Fahrkarte",
        "站台": "der Bahnsteig",
        "出发": "die Abfahrt",
        "到达": "die Ankunft",
        "单程": "einfach",
        "往返": "hin und zurück",
        "护照": "der Reisepass",
        "签证": "das Visum",
        "海关": "der Zoll",
        "机场在哪里？": "Wo ist der Flughafen?",
        "我需要一张去柏林的票。": "Ich brauche eine Fahrkarte nach Berlin.",
        "单程还是往返？": "Einfach oder hin und zurück?",
        "火车从哪个站台出发？": "Von welchem Bahnsteig fährt der Zug ab?",
        "下一班车几点？": "Wann kommt der nächste Bus?",
        "这个座位有人吗？": "Ist dieser Platz frei?",
        "请出示您的护照。": "Ihren Reisepass, bitte.",
        "我没有需要申报的物品。": "Ich habe nichts zu verzollen.",
        "旅途有多久？": "Wie lange dauert die Reise?",
        "请在下一站让我下车。": "Lassen Sie mich bitte an der nächsten Haltestelle aussteigen.",
        # hotel
        "入住": "einchecken",
        "退房": "auschecken",
        "房卡": "der Zimmerschlüssel",
        "单人间": "das Einzelzimmer",
        "双人间": "das Doppelzimmer",
        "预订": "die Reservierung",
        "早餐": "das Frühstück",
        "无线网络": "das WLAN",
        "空调": "die Klimaanlage",
        "客房服务": "der Zimmerservice",
        "我有预订。": "Ich habe eine Reservierung.",
        "我想办理入住。": "Ich möchte bitte einchecken.",
        "双人间一晚多少钱？": "Was kostet ein Doppelzimmer pro Nacht?",
        "包含早餐吗？": "Ist Frühstück inkludiert?",
        "WiFi密码是什么？": "Wie ist das WLAN-Passwort?",
        "空调坏了。": "Die Klimaanlage funktioniert nicht.",
        "能给我设置早上7点的叫醒服务吗？": "Kann ich bitte einen Weckruf um 7 Uhr haben?",
        "我想退房。": "Ich möchte bitte auschecken.",
        "我能寄存行李吗？": "Kann ich mein Gepäck hier lassen?",
        "谢谢，住得很愉快！": "Vielen Dank für einen wundervollen Aufenthalt!",
    }

    es = {
        "我想要": "Quisiera",
        "菜单": "el menú",
        "点餐": "pedir",
        "账单": "la cuenta",
        "美味": "delicioso",
        "推荐": "la recomendación",
        "预约": "la reserva",
        "服务员": "el camarero",
        "两人桌": "una mesa para dos",
        "今日特价": "el plato del día",
        "我想预约。": "Me gustaría hacer una reserva.",
        "请给我一个两人桌。": "Una mesa para dos, por favor.",
        "我能看看菜单吗？": "¿Puedo ver el menú?",
        "你推荐什么？": "¿Qué recomienda?",
        "我要牛排。": "Quiero el filete, por favor.",
        "请给我账单。": "¿Me trae la cuenta, por favor?",
        "食物太好吃了！": "¡La comida está deliciosa!",
        "能给我一些水吗？": "¿Me puede dar un poco de agua?",
        "服务费包含在内吗？": "¿Está incluido el servicio?",
        "我对花生过敏。": "Soy alérgico al cacahuete.",
        # shopping
        "多少钱": "Cuánto",
        "折扣": "el descuento",
        "信用卡": "la tarjeta de crédito",
        "现金": "el efectivo",
        "尺寸": "la talla",
        "颜色": "el color",
        "试穿": "probarse",
        "收据": "el recibo",
        "太贵": "demasiado caro",
        "换货": "cambiar",
        "这个多少钱？": "¿Cuánto cuesta esto?",
        "我能试穿这个吗？": "¿Puedo probármelo?",
        "有别的颜色吗？": "¿Lo tiene en otro color?",
        "太贵了。有折扣吗？": "Es demasiado caro. ¿Hay descuento?",
        "我买了。能用卡支付吗？": "Me lo llevo. ¿Puedo pagar con tarjeta?",
        "请给我收据。": "¿Me da un recibo, por favor?",
        "我想换这个。": "Quisiera cambiar esto.",
        "有小一点的尺寸吗？": "¿Tiene una talla más pequeña?",
        "有打折活动吗？": "¿Hay rebajas?",
        "我就看看，谢谢。": "Sólo estoy mirando, gracias.",
        # travel
        "机场": "el aeropuerto",
        "票": "el billete",
        "站台": "el andén",
        "出发": "la salida",
        "到达": "la llegada",
        "单程": "ida",
        "往返": "ida y vuelta",
        "护照": "el pasaporte",
        "签证": "el visado",
        "海关": "la aduana",
        "机场在哪里？": "¿Dónde está el aeropuerto?",
        "我需要一张去马德里的票。": "Necesito un billete a Madrid.",
        "单程还是往返？": "¿Ida o ida y vuelta?",
        "火车从哪个站台出发？": "¿De qué andén sale el tren?",
        "下一班车几点？": "¿A qué hora sale el próximo autobús?",
        "这个座位有人吗？": "¿Está ocupado este asiento?",
        "请出示您的护照。": "Su pasaporte, por favor.",
        "我没有需要申报的物品。": "No tengo nada que declarar.",
        "旅途有多久？": "¿Cuánto dura el viaje?",
        "请在下一站让我下车。": "Déjeme en la próxima parada, por favor.",
        # hotel
        "入住": "registrarse",
        "退房": "salir",
        "房卡": "la llave de la habitación",
        "单人间": "la habitación individual",
        "双人间": "la habitación doble",
        "预订": "la reserva",
        "早餐": "el desayuno",
        "无线网络": "el WiFi",
        "空调": "el aire acondicionado",
        "客房服务": "el servicio de habitaciones",
        "我有预订。": "Tengo una reserva.",
        "我想办理入住。": "Quisiera registrarme, por favor.",
        "双人间一晚多少钱？": "¿Cuánto cuesta una habitación doble por noche?",
        "包含早餐吗？": "¿Está incluido el desayuno?",
        "WiFi密码是什么？": "¿Cuál es la contraseña del WiFi?",
        "空调坏了。": "El aire acondicionado no funciona.",
        "能给我设置早上7点的叫醒服务吗？": "¿Puede darme una llamada de despertar a las 7?",
        "我想退房。": "Quisiera salir, por favor.",
        "我能寄存行李吗？": "¿Puedo dejar mi equipaje aquí?",
        "谢谢，住得很愉快！": "¡Gracias por una estancia maravillosa!",
    }

    it = {
        "我想要": "Vorrei",
        "菜单": "il menu",
        "点餐": "ordinare",
        "账单": "il conto",
        "美味": "delizioso",
        "推荐": "la raccomandazione",
        "预约": "la prenotazione",
        "服务员": "il cameriere",
        "两人桌": "un tavolo per due",
        "今日特价": "il piatto del giorno",
        "我想预约。": "Vorrei fare una prenotazione.",
        "请给我一个两人桌。": "Un tavolo per due, per favore.",
        "我能看看菜单吗？": "Posso vedere il menu?",
        "你推荐什么？": "Cosa consiglia?",
        "我要牛排。": "Prendo la bistecca, per favore.",
        "请给我账单。": "Posso avere il conto, per favore?",
        "食物太好吃了！": "Il cibo è delizioso!",
        "能给我一些水吗？": "Posso avere un po' d'acqua?",
        "服务费包含在内吗？": "Il servizio è incluso?",
        "我对花生过敏。": "Sono allergico alle arachidi.",
        # shopping
        "多少钱": "Quanto",
        "折扣": "lo sconto",
        "信用卡": "la carta di credito",
        "现金": "il contante",
        "尺寸": "la taglia",
        "颜色": "il colore",
        "试穿": "provare",
        "收据": "lo scontrino",
        "太贵": "troppo caro",
        "换货": "cambiare",
        "这个多少钱？": "Quanto costa questo?",
        "我能试穿这个吗？": "Posso provarlo?",
        "有别的颜色吗？": "Ce l'ha in un altro colore?",
        "太贵了。有折扣吗？": "È troppo caro. C'è uno sconto?",
        "我买了。能用卡支付吗？": "Lo prendo. Posso pagare con la carta?",
        "请给我收据。": "Lo scontrino, per favore.",
        "我想换这个。": "Vorrei cambiare questo.",
        "有小一点的尺寸吗？": "Ha una taglia più piccola?",
        "有打折活动吗？": "Ci sono i saldi?",
        "我就看看，谢谢。": "Sto solo guardando, grazie.",
        # travel
        "机场": "l'aeroporto",
        "票": "il biglietto",
        "站台": "il binario",
        "出发": "la partenza",
        "到达": "l'arrivo",
        "单程": "solo andata",
        "往返": "andata e ritorno",
        "护照": "il passaporto",
        "签证": "il visto",
        "海关": "la dogana",
        "机场在哪里？": "Dov'è l'aeroporto?",
        "我需要一张去罗马的票。": "Ho bisogno di un biglietto per Roma.",
        "单程还是往返？": "Solo andata o andata e ritorno?",
        "火车从哪个站台出发？": "Da quale binario parte il treno?",
        "下一班车几点？": "A che ora parte il prossimo autobus?",
        "这个座位有人吗？": "Questo posto è occupato?",
        "请出示您的护照。": "Il passaporto, per favore.",
        "我没有需要申报的物品。": "Non ho nulla da dichiarare.",
        "旅途有多久？": "Quanto dura il viaggio?",
        "请在下一站让我下车。": "Mi faccia scendere alla prossima fermata, per favore.",
        # hotel
        "入住": "fare il check-in",
        "退房": "fare il check-out",
        "房卡": "la chiave della camera",
        "单人间": "la camera singola",
        "双人间": "la camera doppia",
        "预订": "la prenotazione",
        "早餐": "la colazione",
        "无线网络": "il WiFi",
        "空调": "l'aria condizionata",
        "客房服务": "il servizio in camera",
        "我有预订。": "Ho una prenotazione.",
        "我想办理入住。": "Vorrei fare il check-in, per favore.",
        "双人间一晚多少钱？": "Quanto costa una camera doppia a notte?",
        "包含早餐吗？": "La colazione è inclusa?",
        "WiFi密码是什么？": "Qual è la password del WiFi?",
        "空调坏了。": "L'aria condizionata non funziona.",
        "能给我设置早上7点的叫醒服务吗？": "Posso avere una sveglia alle 7?",
        "我想退房。": "Vorrei fare il check-out, per favore.",
        "我能寄存行李吗？": "Posso lasciare il bagaglio qui?",
        "谢谢，住得很愉快！": "Grazie per un soggiorno meraviglioso!",
    }

    pt = {
        "我想要": "Eu gostaria de",
        "菜单": "o cardápio",
        "点餐": "pedir",
        "账单": "a conta",
        "美味": "delicioso",
        "推荐": "a recomendação",
        "预约": "a reserva",
        "服务员": "o garçom",
        "两人桌": "uma mesa para dois",
        "今日特价": "o prato do dia",
        "我想预约。": "Gostaria de fazer uma reserva.",
        "请给我一个两人桌。": "Uma mesa para dois, por favor.",
        "我能看看菜单吗？": "Posso ver o cardápio?",
        "你推荐什么？": "O que você recomenda?",
        "我要牛排。": "Vou querer o bife, por favor.",
        "请给我账单。": "A conta, por favor.",
        "食物太好吃了！": "A comida está deliciosa!",
        "能给我一些水吗？": "Pode me dar um pouco de água?",
        "服务费包含在内吗？": "O serviço está incluído?",
        "我对花生过敏。": "Sou alérgico a amendoim.",
        # shopping
        "多少钱": "Quanto",
        "折扣": "o desconto",
        "信用卡": "o cartão de crédito",
        "现金": "o dinheiro",
        "尺寸": "o tamanho",
        "颜色": "a cor",
        "试穿": "experimentar",
        "收据": "o recibo",
        "太贵": "muito caro",
        "换货": "trocar",
        "这个多少钱？": "Quanto custa isto?",
        "我能试穿这个吗？": "Posso experimentar?",
        "有别的颜色吗？": "Tem em outra cor?",
        "太贵了。有折扣吗？": "Está muito caro. Tem desconto?",
        "我买了。能用卡支付吗？": "Vou levar. Posso pagar com cartão?",
        "请给我收据。": "O recibo, por favor.",
        "我想换这个。": "Gostaria de trocar isto.",
        "有小一点的尺寸吗？": "Tem um tamanho menor?",
        "有打折活动吗？": "Tem liquidação?",
        "我就看看，谢谢。": "Só estou olhando, obrigado.",
        # travel
        "机场": "o aeroporto",
        "票": "o bilhete",
        "站台": "a plataforma",
        "出发": "a partida",
        "到达": "a chegada",
        "单程": "só ida",
        "往返": "ida e volta",
        "护照": "o passaporte",
        "签证": "o visto",
        "海关": "a alfândega",
        "机场在哪里？": "Onde fica o aeroporto?",
        "我需要一张去里斯本的票。": "Preciso de um bilhete para Lisboa.",
        "单程还是往返？": "Só ida ou ida e volta?",
        "火车从哪个站台出发？": "De qual plataforma o trem sai?",
        "下一班车几点？": "A que horas sai o próximo ônibus?",
        "这个座位有人吗？": "Este lugar está ocupado?",
        "请出示您的护照。": "Seu passaporte, por favor.",
        "我没有需要申报的物品。": "Não tenho nada a declarar.",
        "旅途有多久？": "Quanto tempo dura a viagem?",
        "请在下一站让我下车。": "Me deixe na próxima parada, por favor.",
        # hotel
        "入住": "fazer check-in",
        "退房": "fazer check-out",
        "房卡": "a chave do quarto",
        "单人间": "o quarto individual",
        "双人间": "o quarto duplo",
        "预订": "a reserva",
        "早餐": "o café da manhã",
        "无线网络": "o WiFi",
        "空调": "o ar condicionado",
        "客房服务": "o serviço de quarto",
        "我有预订。": "Tenho uma reserva.",
        "我想办理入住。": "Gostaria de fazer check-in, por favor.",
        "双人间一晚多少钱？": "Quanto custa um quarto duplo por noite?",
        "包含早餐吗？": "O café da manhã está incluído?",
        "WiFi密码是什么？": "Qual é a senha do WiFi?",
        "空调坏了。": "O ar condicionado não está funcionando.",
        "能给我设置早上7点的叫醒服务吗？": "Pode me dar um despertador às 7h?",
        "我想退房。": "Gostaria de fazer check-out, por favor.",
        "我能寄存行李吗？": "Posso deixar minha bagagem aqui?",
        "谢谢，住得很愉快！": "Obrigado por uma estadia maravilhosa!",
    }

    ru = {
        "我想要": "Я хотел бы",
        "菜单": "меню",
        "点餐": "заказать",
        "账单": "счёт",
        "美味": "вкусно",
        "推荐": "рекомендация",
        "预约": "бронирование",
        "服务员": "официант",
        "两人桌": "столик на двоих",
        "今日特价": "блюдо дня",
        "我想预约。": "Я хотел бы забронировать столик.",
        "请给我一个两人桌。": "Столик на двоих, пожалуйста.",
        "我能看看菜单吗？": "Можно посмотреть меню?",
        "你推荐什么？": "Что вы порекомендуете?",
        "我要牛排。": "Я возьму стейк.",
        "请给我账单。": "Счёт, пожалуйста.",
        "食物太好吃了！": "Еда очень вкусная!",
        "能给我一些水吗？": "Можно воды?",
        "服务费包含在内吗？": "Обслуживание включено?",
        "我对花生过敏。": "У меня аллергия на арахис.",
        # shopping
        "多少钱": "Сколько",
        "折扣": "скидка",
        "信用卡": "кредитная карта",
        "现金": "наличные",
        "尺寸": "размер",
        "颜色": "цвет",
        "试穿": "примерить",
        "收据": "чек",
        "太贵": "слишком дорого",
        "换货": "обменять",
        "这个多少钱？": "Сколько это стоит?",
        "我能试穿这个吗？": "Можно примерить?",
        "有别的颜色吗？": "У вас есть другого цвета?",
        "太贵了。有折扣吗？": "Слишком дорого. Есть скидка?",
        "我买了。能用卡支付吗？": "Я беру. Можно оплатить картой?",
        "请给我收据。": "Чек, пожалуйста.",
        "我想换这个。": "Я хотел бы обменять это.",
        "有小一点的尺寸吗？": "У вас есть меньший размер?",
        "有打折活动吗？": "Есть распродажа?",
        "我就看看，谢谢。": "Я просто смотрю, спасибо.",
        # travel
        "机场": "аэропорт",
        "票": "билет",
        "站台": "платформа",
        "出发": "отправление",
        "到达": "прибытие",
        "单程": "в один конец",
        "往返": "туда и обратно",
        "护照": "паспорт",
        "签证": "виза",
        "海关": "таможня",
        "机场在哪里？": "Где находится аэропорт?",
        "我需要一张去莫斯科的票。": "Мне нужен билет в Москву.",
        "单程还是往返？": "В один конец или туда и обратно?",
        "火车从哪个站台出发？": "С какой платформы отправляется поезд?",
        "下一班车几点？": "Во сколько следующий автобус?",
        "这个座位有人吗？": "Это место занято?",
        "请出示您的护照。": "Ваш паспорт, пожалуйста.",
        "我没有需要申报的物品。": "У меня нет ничего для декларации.",
        "旅途有多久？": "Сколько длится поездка?",
        "请在下一站让我下车。": "Высадите меня на следующей остановке, пожалуйста.",
        # hotel
        "入住": "заселиться",
        "退房": "выехать",
        "房卡": "ключ от номера",
        "单人间": "одноместный номер",
        "双人间": "двухместный номер",
        "预订": "бронирование",
        "早餐": "завтрак",
        "无线网络": "WiFi",
        "空调": "кондиционер",
        "客房服务": "обслуживание в номере",
        "我有预订。": "У меня есть бронирование.",
        "我想办理入住。": "Я хотел бы заселиться.",
        "双人间一晚多少钱？": "Сколько стоит двухместный номер за ночь?",
        "包含早餐吗？": "Завтрак включён?",
        "WiFi密码是什么？": "Какой пароль от WiFi?",
        "空调坏了。": "Кондиционер не работает.",
        "能给我设置早上7点的叫醒服务吗？": "Можно заказать пробуждение в 7 утра?",
        "我想退房。": "Я хотел бы выехать.",
        "我能寄存行李吗？": "Можно оставить багаж здесь?",
        "谢谢，住得很愉快！": "Спасибо за прекрасное пребывание!",
    }

    th = {
        "我想要": "ฉันอยากได้",
        "菜单": "เมนู",
        "点餐": "สั่งอาหาร",
        "账单": "บิล",
        "美味": "อร่อย",
        "推荐": "คำแนะนำ",
        "预约": "การจอง",
        "服务员": "พนักงานเสิร์ฟ",
        "两人桌": "โต๊ะสำหรับสองคน",
        "今日特价": "เมนูพิเศษวันนี้",
        "我想预约。": "ฉันต้องการจองโต๊ะ",
        "请给我一个两人桌。": "โต๊ะสำหรับสองคนครับ",
        "我能看看菜单吗？": "ขอดูเมนูหน่อยได้ไหม",
        "你推荐什么？": "คุณแนะนำอะไร",
        "我要牛排。": "ฉันขอสเต็ก",
        "请给我账单。": "เช็คบิลด้วยครับ",
        "食物太好吃了！": "อาหารอร่อยมาก",
        "能给我一些水吗？": "ขอน้ำหน่อยได้ไหม",
        "服务费包含在内吗？": "รวมค่าบริการหรือยัง",
        "我对花生过敏。": "ฉันแพ้ถั่วลิสง",
        # shopping
        "多少钱": "เท่าไหร่",
        "折扣": "ส่วนลด",
        "信用卡": "บัตรเครดิต",
        "现金": "เงินสด",
        "尺寸": "ขนาด",
        "颜色": "สี",
        "试穿": "ลองใส่",
        "收据": "ใบเสร็จ",
        "太贵": "แพงเกินไป",
        "换货": "เปลี่ยนสินค้า",
        "这个多少钱？": "อันนี้เท่าไหร่",
        "我能试穿这个吗？": "ลองใส่ได้ไหม",
        "有别的颜色吗？": "มีสีอื่นไหม",
        "太贵了。有折扣吗？": "แพงเกินไป มีส่วนลดไหม",
        "我买了。能用卡支付吗？": "ฉันเอาอันนี้ จ่ายด้วยบัตรได้ไหม",
        "请给我收据。": "ขอใบเสร็จด้วยครับ",
        "我想换这个。": "ฉันอยากเปลี่ยนอันนี้",
        "有小一点的尺寸吗？": "มีขนาดเล็กกว่านี้ไหม",
        "有打折活动吗？": "มีลดราคาไหม",
        "我就看看，谢谢。": "แค่ดูเฉยๆ ขอบคุณ",
        # travel
        "机场": "สนามบิน",
        "票": "ตั๋ว",
        "站台": "ชานชาลา",
        "出发": "ออกเดินทาง",
        "到达": "ถึง",
        "单程": "เที่ยวเดียว",
        "往返": "ไป-กลับ",
        "护照": "พาสปอร์ต",
        "签证": "วีซ่า",
        "海关": "ศุลกากร",
        "机场在哪里？": "สนามบินอยู่ที่ไหน",
        "我需要一张去曼谷的票。": "ฉันต้องการตั๋วไปกรุงเทพ",
        "单程还是往返？": "เที่ยวเดียวหรือไปกลับ",
        "火车从哪个站台出发？": "รถไฟออกจากชานชาลาไหน",
        "下一班车几点？": "รถเที่ยวหน้าไปกี่โมง",
        "这个座位有人吗？": "ที่นั่งนี้มีคนหรือยัง",
        "请出示您的护照。": "ขอดูพาสปอร์ตด้วยครับ",
        "我没有需要申报的物品。": "ฉันไม่มีของต้องแจ้งศุลกากร",
        "旅途有多久？": "เดินทางนานแค่ไหน",
        "请在下一站让我下车。": "ลงป้ายหน้าด้วยครับ",
        # hotel
        "入住": "เช็คอิน",
        "退房": "เช็คเอาท์",
        "房卡": "กุญแจห้อง",
        "单人间": "ห้องเดี่ยว",
        "双人间": "ห้องคู่",
        "预订": "การจอง",
        "早餐": "อาหารเช้า",
        "无线网络": "WiFi",
        "空调": "แอร์",
        "客房服务": "รูมเซอร์วิส",
        "我有预订。": "ฉันจองห้องไว้แล้ว",
        "我想办理入住。": "ฉันขอเช็คอินครับ",
        "双人间一晚多少钱？": "ห้องคู่คืนละเท่าไหร่",
        "包含早餐吗？": "รวมอาหารเช้าไหม",
        "WiFi密码是什么？": "รหัส WiFi คืออะไร",
        "空调坏了。": "แอร์เสีย",
        "能给我设置早上7点的叫醒服务吗？": "ช่วยปลุกตอน 7 โมงได้ไหม",
        "我想退房。": "ฉันขอเช็คเอาท์",
        "我能寄存行李吗？": "ฝากกระเป๋าไว้ที่นี่ได้ไหม",
        "谢谢，住得很愉快！": "ขอบคุณสำหรับการต้อนรับที่ดี",
    }

    langs = {
        "de": de, "German": de,
        "es": es, "Spanish": es,
        "it": it, "Italian": it,
        "pt": pt, "Portuguese": pt,
        "ru": ru, "Russian": ru,
        "th": th, "Thai": th,
        "en": {}, "English": {},
        "ja": {}, "Japanese": {},
        "ko": {}, "Korean": {},
        "fr": {}, "French": {},
    }

    tr = langs.get(lang_label, langs.get("en", {}))

    def _translate(phrase_text, cn_text):
        """Translate English phrase to target language. Falls back to English phrase itself if no trans."""
        if tr:
            return tr.get(cn_text, phrase_text)
        return phrase_text

    def _translate_word(word_text, cn_text):
        """Translate English word to target language."""
        if tr:
            return tr.get(cn_text, word_text)
        return word_text

    skills = []

    for skill_key, skill_data in conv_base["en"].items():
        skill_name = {
            "restaurant": "Restaurant Dialogues",
            "shopping": "Shopping Dialogues",
            "travel": "Travel Dialogues",
            "hotel": "Hotel & Accommodation",
        }[skill_key]

        words = []
        for w in skill_data["words"]:
            words.append({
                "word": _translate_word(w["word"], w["translation"]),
                "translation": w["translation"],
            })

        phrases = []
        for p in skill_data["phrases"]:
            phrases.append({
                "phrase": _translate(p["phrase"], p["translation"]),
                "translation": p["translation"],
            })

        # Build mini-dictionary
        mini_dict = {lang_name: [], "Chinese": []}
        for w in skill_data["words"]:
            target_word = _translate_word(w["word"], w["translation"])
            mini_dict.setdefault(lang_name, []).append(f"{target_word}: {w['translation']}")
            mini_dict.setdefault("Chinese", []).append(f"{w['translation']}: {target_word}")
        for k in mini_dict:
            mini_dict[k] = list(set(mini_dict[k]))

        skills.append({
            "name": skill_name,
            "special_chars": [],
            "words": words,
            "phrases": phrases,
            "mini_dictionary": mini_dict,
        })

    return skills


# ── Course Definitions ──

def define_courses():
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
            {
                "name": "Conversations",
                "skills": conversation_skills("English", "en"),
            },
        ],
    }

    zh_ja = {
        "name": "Japanese",
        "code": "ja",
        "for_speakers_of": "Chinese",
        "special_chars": ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ"],
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
            {
                "name": "Conversations",
                "skills": conversation_skills("Japanese", "ja"),
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
            {
                "name": "Conversations",
                "skills": conversation_skills("Korean", "ko"),
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
            {
                "name": "Conversations",
                "skills": conversation_skills("French", "fr"),
            },
        ],
    }

    # ── New languages ──

    zh_de = {
        "name": "German",
        "code": "de",
        "for_speakers_of": "Chinese",
        "special_chars": ["ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "Hallo", "translation": "你好"},
                            {"word": "Tschüss", "translation": "再见"},
                            {"word": "Guten Morgen", "translation": "早上好"},
                            {"word": "Guten Abend", "translation": "晚上好"},
                            {"word": "Danke", "translation": "谢谢"},
                            {"word": "Bitte", "translation": "请/不客气"},
                            {"word": "Entschuldigung", "translation": "对不起"},
                            {"word": "Ja", "translation": "是的"},
                            {"word": "Nein", "translation": "不是"},
                            {"word": "Wie geht's", "translation": "你好吗"},
                        ],
                        "phrases": [
                            {"phrase": "Hallo, wie geht's?", "translation": "你好，你好吗？"},
                            {"phrase": "Guten Morgen, danke.", "translation": "早上好，谢谢。"},
                            {"phrase": "Tschüss, bis später.", "translation": "再见，回头见。"},
                            {"phrase": "Danke schön!", "translation": "非常感谢！"},
                            {"phrase": "Entschuldigung, wo ist der Bahnhof?", "translation": "对不起，车站在哪里？"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": [],
                        "words": [
                            {"word": "eins", "translation": "一"},
                            {"word": "zwei", "translation": "二"},
                            {"word": "drei", "translation": "三"},
                            {"word": "vier", "translation": "四"},
                            {"word": "fünf", "translation": "五"},
                            {"word": "sechs", "translation": "六"},
                            {"word": "sieben", "translation": "七"},
                            {"word": "acht", "translation": "八"},
                            {"word": "neun", "translation": "九"},
                            {"word": "zehn", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "Eins, zwei, drei.", "translation": "一、二、三。"},
                            {"phrase": "Es ist fünf Uhr.", "translation": "现在五点钟。"},
                            {"phrase": "Zehn Personen.", "translation": "有十个人。"},
                        ],
                    },
                ],
            },
            {
                "name": "Food & Drink",
                "skills": [
                    {
                        "name": "Basic Foods",
                        "special_chars": ["ä"],
                        "words": [
                            {"word": "Wasser", "translation": "水"},
                            {"word": "Brot", "translation": "面包"},
                            {"word": "Reis", "translation": "米饭"},
                            {"word": "Milch", "translation": "牛奶"},
                            {"word": "Ei", "translation": "鸡蛋"},
                            {"word": "Hähnchen", "translation": "鸡肉"},
                            {"word": "Fisch", "translation": "鱼"},
                            {"word": "Obst", "translation": "水果"},
                            {"word": "Gemüse", "translation": "蔬菜"},
                            {"word": "Tee", "translation": "茶"},
                            {"word": "Kaffee", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "Ich möchte Wasser.", "translation": "我想要水。"},
                            {"phrase": "Brot und Milch, bitte.", "translation": "请给我面包和牛奶。"},
                            {"phrase": "Ich mag Reis.", "translation": "我喜欢米饭。"},
                            {"phrase": "Das schmeckt gut.", "translation": "这个很好吃。"},
                        ],
                    },
                ],
            },
            {
                "name": "Conversations",
                "skills": conversation_skills("German", "de"),
            },
        ],
    }

    zh_es = {
        "name": "Spanish",
        "code": "es",
        "for_speakers_of": "Chinese",
        "special_chars": ["á", "é", "í", "ó", "ú", "ü", "ñ", "¿", "¡"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "hola", "translation": "你好"},
                            {"word": "adiós", "translation": "再见"},
                            {"word": "buenos días", "translation": "早上好"},
                            {"word": "buenas tardes", "translation": "下午好"},
                            {"word": "gracias", "translation": "谢谢"},
                            {"word": "por favor", "translation": "请"},
                            {"word": "perdón", "translation": "对不起"},
                            {"word": "sí", "translation": "是的"},
                            {"word": "no", "translation": "不是"},
                            {"word": "de nada", "translation": "不客气"},
                        ],
                        "phrases": [
                            {"phrase": "¡Hola! ¿Cómo estás?", "translation": "你好！你好吗？"},
                            {"phrase": "Buenos días, gracias.", "translation": "早上好，谢谢。"},
                            {"phrase": "Adiós, hasta luego.", "translation": "再见，回头见。"},
                            {"phrase": "Muchas gracias.", "translation": "非常感谢。"},
                            {"phrase": "Perdón, ¿dónde está el baño?", "translation": "对不起，洗手间在哪里？"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": ["á", "é"],
                        "words": [
                            {"word": "uno", "translation": "一"},
                            {"word": "dos", "translation": "二"},
                            {"word": "tres", "translation": "三"},
                            {"word": "cuatro", "translation": "四"},
                            {"word": "cinco", "translation": "五"},
                            {"word": "seis", "translation": "六"},
                            {"word": "siete", "translation": "七"},
                            {"word": "ocho", "translation": "八"},
                            {"word": "nueve", "translation": "九"},
                            {"word": "diez", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "Uno, dos, tres.", "translation": "一、二、三。"},
                            {"phrase": "Son las cinco.", "translation": "现在五点钟。"},
                            {"phrase": "Hay diez personas.", "translation": "有十个人。"},
                        ],
                    },
                ],
            },
            {
                "name": "Food & Drink",
                "skills": [
                    {
                        "name": "Basic Foods",
                        "special_chars": ["é", "á"],
                        "words": [
                            {"word": "agua", "translation": "水"},
                            {"word": "pan", "translation": "面包"},
                            {"word": "arroz", "translation": "米饭"},
                            {"word": "leche", "translation": "牛奶"},
                            {"word": "huevo", "translation": "鸡蛋"},
                            {"word": "pollo", "translation": "鸡肉"},
                            {"word": "pescado", "translation": "鱼"},
                            {"word": "fruta", "translation": "水果"},
                            {"word": "verdura", "translation": "蔬菜"},
                            {"word": "té", "translation": "茶"},
                            {"word": "café", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "Quiero agua.", "translation": "我想要水。"},
                            {"phrase": "Pan y leche, por favor.", "translation": "请给我面包和牛奶。"},
                            {"phrase": "Me gusta el arroz.", "translation": "我喜欢米饭。"},
                            {"phrase": "Está delicioso.", "translation": "这个很好吃。"},
                        ],
                    },
                ],
            },
            {
                "name": "Conversations",
                "skills": conversation_skills("Spanish", "es"),
            },
        ],
    }

    zh_it = {
        "name": "Italian",
        "code": "it",
        "for_speakers_of": "Chinese",
        "special_chars": ["à", "è", "é", "ì", "ò", "ù"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "ciao", "translation": "你好/再见"},
                            {"word": "buongiorno", "translation": "早上好"},
                            {"word": "buonasera", "translation": "晚上好"},
                            {"word": "grazie", "translation": "谢谢"},
                            {"word": "per favore", "translation": "请"},
                            {"word": "scusa", "translation": "对不起"},
                            {"word": "sì", "translation": "是的"},
                            {"word": "no", "translation": "不是"},
                            {"word": "prego", "translation": "不客气"},
                            {"word": "arrivederci", "translation": "再见（正式）"},
                        ],
                        "phrases": [
                            {"phrase": "Ciao! Come stai?", "translation": "你好！你好吗？"},
                            {"phrase": "Buongiorno, grazie.", "translation": "早上好，谢谢。"},
                            {"phrase": "Arrivederci, a presto.", "translation": "再见，回头见。"},
                            {"phrase": "Mille grazie!", "translation": "非常感谢！"},
                            {"phrase": "Scusa, dov'è il bagno?", "translation": "对不起，洗手间在哪里？"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": [],
                        "words": [
                            {"word": "uno", "translation": "一"},
                            {"word": "due", "translation": "二"},
                            {"word": "tre", "translation": "三"},
                            {"word": "quattro", "translation": "四"},
                            {"word": "cinque", "translation": "五"},
                            {"word": "sei", "translation": "六"},
                            {"word": "sette", "translation": "七"},
                            {"word": "otto", "translation": "八"},
                            {"word": "nove", "translation": "九"},
                            {"word": "dieci", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "Uno, due, tre.", "translation": "一、二、三。"},
                            {"phrase": "Sono le cinque.", "translation": "现在五点钟。"},
                            {"phrase": "Ci sono dieci persone.", "translation": "有十个人。"},
                        ],
                    },
                ],
            },
            {
                "name": "Food & Drink",
                "skills": [
                    {
                        "name": "Basic Foods",
                        "special_chars": ["ò", "è"],
                        "words": [
                            {"word": "acqua", "translation": "水"},
                            {"word": "pane", "translation": "面包"},
                            {"word": "riso", "translation": "米饭"},
                            {"word": "latte", "translation": "牛奶"},
                            {"word": "uovo", "translation": "鸡蛋"},
                            {"word": "pollo", "translation": "鸡肉"},
                            {"word": "pesce", "translation": "鱼"},
                            {"word": "frutta", "translation": "水果"},
                            {"word": "verdura", "translation": "蔬菜"},
                            {"word": "tè", "translation": "茶"},
                            {"word": "caffè", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "Vorrei dell'acqua.", "translation": "我想要水。"},
                            {"phrase": "Pane e latte, per favore.", "translation": "请给我面包和牛奶。"},
                            {"phrase": "Mi piace il riso.", "translation": "我喜欢米饭。"},
                            {"phrase": "È delizioso.", "translation": "这个很好吃。"},
                        ],
                    },
                ],
            },
            {
                "name": "Conversations",
                "skills": conversation_skills("Italian", "it"),
            },
        ],
    }

    zh_pt = {
        "name": "Portuguese",
        "code": "pt",
        "for_speakers_of": "Chinese",
        "special_chars": ["á", "à", "â", "ã", "ç", "é", "ê", "í", "ó", "ô", "õ", "ú"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "olá", "translation": "你好"},
                            {"word": "tchau", "translation": "再见"},
                            {"word": "bom dia", "translation": "早上好"},
                            {"word": "boa tarde", "translation": "下午好"},
                            {"word": "obrigado", "translation": "谢谢"},
                            {"word": "por favor", "translation": "请"},
                            {"word": "desculpe", "translation": "对不起"},
                            {"word": "sim", "translation": "是的"},
                            {"word": "não", "translation": "不是"},
                            {"word": "de nada", "translation": "不客气"},
                        ],
                        "phrases": [
                            {"phrase": "Olá! Como vai?", "translation": "你好！你好吗？"},
                            {"phrase": "Bom dia, obrigado.", "translation": "早上好，谢谢。"},
                            {"phrase": "Tchau, até logo.", "translation": "再见，回头见。"},
                            {"phrase": "Muito obrigado!", "translation": "非常感谢！"},
                            {"phrase": "Desculpe, onde fica o banheiro?", "translation": "对不起，洗手间在哪里？"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": ["ã"],
                        "words": [
                            {"word": "um", "translation": "一"},
                            {"word": "dois", "translation": "二"},
                            {"word": "três", "translation": "三"},
                            {"word": "quatro", "translation": "四"},
                            {"word": "cinco", "translation": "五"},
                            {"word": "seis", "translation": "六"},
                            {"word": "sete", "translation": "七"},
                            {"word": "oito", "translation": "八"},
                            {"word": "nove", "translation": "九"},
                            {"word": "dez", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "Um, dois, três.", "translation": "一、二、三。"},
                            {"phrase": "São cinco horas.", "translation": "现在五点钟。"},
                            {"phrase": "Há dez pessoas.", "translation": "有十个人。"},
                        ],
                    },
                ],
            },
            {
                "name": "Food & Drink",
                "skills": [
                    {
                        "name": "Basic Foods",
                        "special_chars": ["á", "ç", "ê", "ã"],
                        "words": [
                            {"word": "água", "translation": "水"},
                            {"word": "pão", "translation": "面包"},
                            {"word": "arroz", "translation": "米饭"},
                            {"word": "leite", "translation": "牛奶"},
                            {"word": "ovo", "translation": "鸡蛋"},
                            {"word": "frango", "translation": "鸡肉"},
                            {"word": "peixe", "translation": "鱼"},
                            {"word": "fruta", "translation": "水果"},
                            {"word": "legume", "translation": "蔬菜"},
                            {"word": "chá", "translation": "茶"},
                            {"word": "café", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "Quero água.", "translation": "我想要水。"},
                            {"phrase": "Pão e leite, por favor.", "translation": "请给我面包和牛奶。"},
                            {"phrase": "Gosto de arroz.", "translation": "我喜欢米饭。"},
                            {"phrase": "Está delicioso.", "translation": "这个很好吃。"},
                        ],
                    },
                ],
            },
            {
                "name": "Conversations",
                "skills": conversation_skills("Portuguese", "pt"),
            },
        ],
    }

    zh_ru = {
        "name": "Russian",
        "code": "ru",
        "for_speakers_of": "Chinese",
        "special_chars": ["Ё", "ё", "Ж", "ж", "Ц", "ц", "Ч", "ч", "Ш", "ш", "Щ", "щ", "ъ", "ь"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "Здравствуйте", "translation": "你好（正式）"},
                            {"word": "Привет", "translation": "你好（非正式）"},
                            {"word": "До свидания", "translation": "再见"},
                            {"word": "Спасибо", "translation": "谢谢"},
                            {"word": "Пожалуйста", "translation": "请/不客气"},
                            {"word": "Извините", "translation": "对不起"},
                            {"word": "Да", "translation": "是的"},
                            {"word": "Нет", "translation": "不是"},
                            {"word": "Как дела?", "translation": "你好吗"},
                            {"word": "Хорошо", "translation": "很好"},
                        ],
                        "phrases": [
                            {"phrase": "Здравствуйте! Как дела?", "translation": "你好！你好吗？"},
                            {"phrase": "Доброе утро, спасибо.", "translation": "早上好，谢谢。"},
                            {"phrase": "До свидания, до встречи.", "translation": "再见，回头见。"},
                            {"phrase": "Большое спасибо!", "translation": "非常感谢！"},
                            {"phrase": "Извините, где туалет?", "translation": "对不起，洗手间在哪里？"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": [],
                        "words": [
                            {"word": "один", "translation": "一"},
                            {"word": "два", "translation": "二"},
                            {"word": "три", "translation": "三"},
                            {"word": "четыре", "translation": "四"},
                            {"word": "пять", "translation": "五"},
                            {"word": "шесть", "translation": "六"},
                            {"word": "семь", "translation": "七"},
                            {"word": "восемь", "translation": "八"},
                            {"word": "девять", "translation": "九"},
                            {"word": "десять", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "Один, два, три.", "translation": "一、二、三。"},
                            {"phrase": "Сейчас пять часов.", "translation": "现在五点钟。"},
                            {"phrase": "Десять человек.", "translation": "有十个人。"},
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
                            {"word": "вода", "translation": "水"},
                            {"word": "хлеб", "translation": "面包"},
                            {"word": "рис", "translation": "米饭"},
                            {"word": "молоко", "translation": "牛奶"},
                            {"word": "яйцо", "translation": "鸡蛋"},
                            {"word": "курица", "translation": "鸡肉"},
                            {"word": "рыба", "translation": "鱼"},
                            {"word": "фрукты", "translation": "水果"},
                            {"word": "овощи", "translation": "蔬菜"},
                            {"word": "чай", "translation": "茶"},
                            {"word": "кофе", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "Я хочу воды.", "translation": "我想要水。"},
                            {"phrase": "Хлеб и молоко, пожалуйста.", "translation": "请给我面包和牛奶。"},
                            {"phrase": "Мне нравится рис.", "translation": "我喜欢米饭。"},
                            {"phrase": "Это вкусно.", "translation": "这个很好吃。"},
                        ],
                    },
                ],
            },
            {
                "name": "Conversations",
                "skills": conversation_skills("Russian", "ru"),
            },
        ],
    }

    zh_th = {
        "name": "Thai",
        "code": "th",
        "for_speakers_of": "Chinese",
        "special_chars": ["ก", "ข", "ค", "ง", "จ", "ฉ", "ช", "ซ", "ด", "ต", "ท", "น", "บ", "ป", "พ", "ม", "ย", "ร", "ล", "ว", "ส", "อ", "ห"],
        "modules": [
            {
                "name": "Basics",
                "skills": [
                    {
                        "name": "Greetings",
                        "words": [
                            {"word": "สวัสดี", "translation": "你好"},
                            {"word": "ลาก่อน", "translation": "再见"},
                            {"word": "อรุณสวัสดิ์", "translation": "早上好"},
                            {"word": "ขอบคุณ", "translation": "谢谢"},
                            {"word": "กรุณา", "translation": "请"},
                            {"word": "ขอโทษ", "translation": "对不起"},
                            {"word": "ใช่", "translation": "是的"},
                            {"word": "ไม่ใช่", "translation": "不是"},
                            {"word": "ไม่เป็นไร", "translation": "没关系/不客气"},
                            {"word": "สบายดีไหม", "translation": "你好吗"},
                        ],
                        "phrases": [
                            {"phrase": "สวัสดีครับ สบายดีไหม", "translation": "你好，你好吗？"},
                            {"phrase": "อรุณสวัสดิ์ครับ ขอบคุณ", "translation": "早上好，谢谢。"},
                            {"phrase": "ลาก่อน แล้วเจอกัน", "translation": "再见，回头见。"},
                            {"phrase": "ขอบคุณมากครับ", "translation": "非常感谢。"},
                            {"phrase": "ขอโทษครับ ห้องน้ำอยู่ที่ไหน", "translation": "对不起，洗手间在哪里？"},
                        ],
                    },
                    {
                        "name": "Numbers",
                        "special_chars": [],
                        "words": [
                            {"word": "หนึ่ง", "translation": "一"},
                            {"word": "สอง", "translation": "二"},
                            {"word": "สาม", "translation": "三"},
                            {"word": "สี่", "translation": "四"},
                            {"word": "ห้า", "translation": "五"},
                            {"word": "หก", "translation": "六"},
                            {"word": "เจ็ด", "translation": "七"},
                            {"word": "แปด", "translation": "八"},
                            {"word": "เก้า", "translation": "九"},
                            {"word": "สิบ", "translation": "十"},
                        ],
                        "phrases": [
                            {"phrase": "หนึ่ง สอง สาม", "translation": "一、二、三。"},
                            {"phrase": "ตอนนี้ห้าโมง", "translation": "现在五点钟。"},
                            {"phrase": "มีสิบคน", "translation": "有十个人。"},
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
                            {"word": "น้ำ", "translation": "水"},
                            {"word": "ขนมปัง", "translation": "面包"},
                            {"word": "ข้าว", "translation": "米饭"},
                            {"word": "นม", "translation": "牛奶"},
                            {"word": "ไข่", "translation": "鸡蛋"},
                            {"word": "ไก่", "translation": "鸡肉"},
                            {"word": "ปลา", "translation": "鱼"},
                            {"word": "ผลไม้", "translation": "水果"},
                            {"word": "ผัก", "translation": "蔬菜"},
                            {"word": "ชา", "translation": "茶"},
                            {"word": "กาแฟ", "translation": "咖啡"},
                        ],
                        "phrases": [
                            {"phrase": "ขอน้ำหน่อยครับ", "translation": "我想要水。"},
                            {"phrase": "ขอขนมปังกับนมครับ", "translation": "请给我面包和牛奶。"},
                            {"phrase": "ฉันชอบข้าว", "translation": "我喜欢米饭。"},
                            {"phrase": "อร่อยมาก", "translation": "这个很好吃。"},
                        ],
                    },
                ],
            },
            {
                "name": "Conversations",
                "skills": conversation_skills("Thai", "th"),
            },
        ],
    }

    return {
        "zh-en": zh_en,
        "zh-ja": zh_ja,
        "zh-ko": zh_ko,
        "zh-fr": zh_fr,
        "zh-de": zh_de,
        "zh-es": zh_es,
        "zh-it": zh_it,
        "zh-pt": zh_pt,
        "zh-ru": zh_ru,
        "zh-th": zh_th,
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
