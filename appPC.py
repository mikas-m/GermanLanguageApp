from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
import sys, os, sqlite3
import pandas as pd
import kivymd.icon_definitions
from kivy.resources import resource_add_path
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText, MDSnackbarButtonContainer, MDSnackbarCloseButton
from kivy.metrics import dp


class Proba(ScreenManager):
    pass


class Dictionary(Screen):
    def submit(self):
        self.clear_input_messages()
        german_word = self.root.ids.german_word.text
        croatian_word = self.root.ids.croatian_word.text

        self.error_message(german_word, 'message_check_verb', 'German word...')
        self.error_message(croatian_word, 'message_check_verb', 'Croatian word...')

        self.insert_word(german_word, croatian_word)
        self.clear_inputs()
        self.clear_checkboxes()

    def delete(self):
        self.clear_input_messages()
        word = self.root.ids.delete_word.text
        croatian_word = self.show_word(word, 'croatian_word', 'words')
        german_word = self.show_word(word, 'german_word', 'words')

        if not word:
            self.root.ids.message_submit.text = "Type in something!"
            return

        if croatian_word is None and german_word is None:
            self.root.ids.message_submit.text = "No word in dictionary!"
        else:
            self.delete_word(word)
            self.clear_inputs()
            self.clear_checkboxes()


class Translation(Screen):
    def show_word_german(self):
        self.clear_checkboxes()
        self.clear_input_messages()
        self.clear_inputs()
        self.show_random_word('german_word', 'words', 'word_translate', 'message_check')

    def show_word_croatian(self):
        self.clear_checkboxes()
        self.clear_input_messages()
        self.clear_inputs()
        self.show_random_word('croatian_word', 'words', 'word_translate', 'message_check')

    def show_translation(self, instance, value):
        self.clear_input_messages()
        word = self.root.ids.word_translate.text
        random_german_word = self.show_word(word, 'german_word', 'words')
        random_croatian_word = self.show_word(word, 'croatian_word', 'words')
        croatian_translation = self.show_matched_word(word, 'croatian_word', 'german_word', 'words', 'word_translated')
        german_translation = self.show_matched_word(word, 'german_word', 'croatian_word', 'words', 'word_translated')

        if value is True:
            self.error_message(word, 'message_check_verb', 'Type something or choose random new word to translate!')
            if random_german_word:
                croatian_translation
            elif random_croatian_word:
                german_translation
            else:
                self.root.ids.message_check.text = 'No word in dictionary!'
        else:
            self.clear_checkboxes()
            self.clear_inputs()
            self.clear_input_messages()

    def check_word(self):
        self.clear_input_messages()
        word = self.root.ids.word_translate.text
        translated_word = self.root.ids.word_translated.text

        german_word = self.show_word(word, 'german_word', 'words')
        croatian_word = self.show_word(word, 'croatian_word', 'words')
        croatian_translation = self.check_matched_word(word, 'croatian_word', 'german_word', 'words', 'word_translated')
        german_translation = self.check_matched_word(word, 'german_word', 'croatian_word', 'words', 'word_translated')

        self.error_message(word, 'message_check_verb', 'Type something or choose random new verb to translate!')
        self.error_message(translated_word, 'message_check_verb', 'Give it a try!')

        if german_word or croatian_word:
            if croatian_translation == translated_word or german_translation == translated_word:
                self.root.ids.message_check.text = 'Nice!'
            else:
                self.root.ids.message_check.text = 'Wrong!'
        else:
            self.root.ids.message_check.text = 'Not a word in dictionary!'


class Verbs(Screen):
    def show_verb(self):
        self.clear_checkboxes()
        self.clear_input_messages()
        self.clear_inputs()
        self.show_random_word('infinitive', 'verbs', 'deutches_verb', 'message_check_verb')

    def check_infinitive(self):
        self.clear_input_messages()
        word = self.root.ids.deutches_verb.text
        infinitive = self.check_matched_word(word, 'second_third_infinitive', 'infinitive', 'verbs')
        user_infinitive = self.root.ids.sec_third.text

        self.check_value(word, infinitive, user_infinitive, 'message_check_verb',
                         'Type something or choose random new verb to translate!',
                         'Not an irregular verb!', 'Give it a try!')

    def show_infinitive(self, instance, value):
        self.clear_input_messages()
        word = self.root.ids.deutches_verb.text
        infinitive = self.show_matched_word(word, 'second_third_infinitive', 'infinitive', 'verbs', 'sec_third')

        self.value_checkboxes(value, word, infinitive,
                        'message_check_verb', 'Type something or choose random new verb to translate!',
                        'Not an irregular verb!')

    def check_preterit(self):
        self.clear_input_messages()
        word = self.root.ids.deutches_verb.text
        preterit = self.check_matched_word(word, 'preterit', 'infinitive', 'verbs', 'preterit')
        user_preterit = self.root.ids.preterit.text

        self.check_value(word, preterit, user_preterit, 'message_check_verb',
                         'Type something or choose random new verb to translate!',
                         'Not an irregular verb!', 'Give it a try!')

    def show_preterit(self, instance, value):
        self.clear_input_messages()
        word = self.root.ids.deutches_verb.text
        preterit = self.show_matched_word(word, 'preterit', 'infinitive', 'verbs', 'preterit')

        self.value_checkboxes(value, word, preterit,
                        'message_check_verb', 'Type something or choose random new verb to translate!',
                        'Not an irregular verb!')

    def check_perfekt(self):
        self.clear_input_messages()
        word = self.root.ids.deutches_verb.text
        perfekt = self.check_matched_word(word, 'perfekt', 'infinitive', 'verbs', 'perfekt')
        user_perfekt = self.root.ids.perfekt.text

        self.check_value(word, perfekt, user_perfekt, 'message_check_verb',
                         'Type something or choose random new verb to translate!',
                         'Not an irregular verb!', 'Give it a try!')

    def show_perfekt(self, instance, value):
        self.clear_input_messages()
        word = self.root.ids.deutches_verb.text
        perfekt = self.show_matched_word(word, 'perfekt', 'infinitive', 'verbs', 'perfekt')

        self.value_checkboxes(value, word, perfekt,
                        'message_check_verb', 'Type something or choose random new verb to translate!',
                        'Not an irregular verb!')

    def check_translation(self):
        self.clear_input_messages()
        word = self.root.ids.deutches_verb.text
        user_translation = self.root.ids.translation.text
        infinitive = self.show_word(word, 'infinitive', 'verbs')
        croatian_translation = self.check_matched_word(word, 'translation', 'infinitive', 'verbs')

        self.error_message(word, 'message_check_verb', 'Type something or choose random new verb to translate!')
        self.error_message(infinitive, 'message_check_verb', 'Not an irregular verb!')
        self.error_message(user_translation, 'message_check_verb', 'Give it a try!')

        croatian_translation = self.check_matched_word(word, 'translation', 'infinitive', 'verbs')

        if croatian_translation == user_translation:
            self.root.ids.message_check_verb.text = 'Nice!'
        else:
            self.root.ids.message_check_verb.text = 'Wrong!'

    def show_translation_verb(self, instance, value):
        self.clear_input_messages()
        word = self.root.ids.deutches_verb.text
        translation = self.show_matched_word(word, 'translation', 'infinitive', 'verbs', 'translation')

        self.value_checkboxes(value, word, translation,
                        'message_check_verb', 'Type something or choose random new verb to translate!',
                        'Not an irregular verb!')

    def check_verb(self):
        word = self.root.ids.deutches_verb.text
        infinitive = self.show_word(word, 'infinitive', 'verbs')

        self.error_message(word, 'message_check_verb', 'Type something or choose random new verb to translate!')
        self.error_message(infinitive, 'message_check_verb', 'Not an irregular verb!')

        user_sec_third = self.root.ids.sec_third.text
        user_preterit = self.root.ids.preterit.text
        user_perfekt = self.root.ids.perfekt.text
        user_translation = self.root.ids.translation.text
        user_words = [
            self.root.ids.sec_third.text, self.root.ids.preterit.text, self.root.ids.perfekt.text, self.root.ids.translation.text
        ]

        if not all(user_words):
            self.root.ids.message_check_verb.text = 'Please provide all the required verbs.'
            return

        sec_third = self.check_matched_word(word, 'second_third_infinitive', 'infinitive', 'verbs')
        preterit = self.check_matched_word(word, 'preterit', 'infinitive', 'verbs')
        perfekt = self.check_matched_word(word, 'perfekt', 'infinitive', 'verbs')
        translation = self.check_matched_word(word, 'translation', 'infinitive', 'verbs')

        message = ""

        if user_sec_third != sec_third:
            message += 'Infinitive exception is wrong!\n'
        else:
            message += 'Infinitive exception is good!\n'
        if user_preterit != preterit:
            message += 'Preterit is wrong!\n'
        else:
            message += 'Preterit is good!\n'
        if user_perfekt != perfekt:
            message += 'Perfekt is wrong!\n'
        else:
            message += 'Perfekt is good!\n'
        if user_translation != translation:
            message += 'Translation is wrong!\n'
        else:
            message += 'Translation is good!\n'

        self.root.ids.message_check_verb.text = message.strip()


class GermanLanguage(MDApp, Dictionary, Translation, Verbs):
    def build(self):
        self.theme_cls.primary_palette = "Azure"
        excel_file = "german_verbs.xlsx"
        df = pd.read_excel(excel_file)
        conn = sqlite3.connect('gwords.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists words(
            german_word text,
            croatian_word text)
        """)
        c.execute("""CREATE TABLE if not exists verbs(
             infinitive text,
             second_third_infinitive text,
             preterit text,
             perfekt text,
             translation text)
        """)
        df.to_sql('verbs', conn, if_exists='append', index=False)
        c.execute("DELETE FROM verbs WHERE ROWID NOT IN (SELECT MIN(ROWID) FROM verbs GROUP BY infinitive)")
        conn.commit()
        conn.close()
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        Builder.load_file("appPC.kv")
        return Proba()

    def clear_inputs(self):
        input_ids = [
            'german_word', 'croatian_word', 'word',
            'word_translate', 'word_translated', 'deutches_verb', 'sec_third',
            'preterit', 'perfekt', 'translation'
        ]
        for input_id in input_ids:
            if input_id in self.root.ids:
                self.root.ids[input_id].text = ''

    def clear_input_messages(self):
        input_messages = [
            'message_submit', 'message_check', 'message_check_verb'
        ]
        for input_message in input_messages:
            if input_message in self.root.ids:
                self.root.ids[input_message].text = ''

    def clear_checkboxes(self):
        checkboxes = [
            'trans_check', 'check_inf', 'check_pret',
            'check_perf', 'check_transl'
        ]
        for checkboxe in checkboxes:
            if checkboxe in self.root.ids:
                self.root.ids[checkboxe].active = False

    def insert_word(self, german_word, croatian_word):
        conn = sqlite3.connect('gwords.db')
        c = conn.cursor()
        c.execute("INSERT INTO words VALUES (?, ?)", (german_word, croatian_word))
        self.root.ids.message_submit.text = "Great job, words added!"
        self.root.ids.german_word.text = ''
        self.root.ids.croatian_word.text = ''
        conn.commit()
        conn.close()

    def delete_word(self, word):
        conn = sqlite3.connect('gwords.db')
        c = conn.cursor()
        c.execute("DELETE FROM words WHERE croatian_word=?",
                     (word,))
        c.execute("DELETE FROM words WHERE german_word=?",
                  (word,))
        self.root.ids.message_submit.text = "Words deleted"
        conn.commit()
        conn.close()

    def show_random_word(self, column, table, message_line, message_error):
        with sqlite3.connect('gwords.db') as conn:
            c = conn.cursor()
            c.execute(f"SELECT {column} FROM {table} ORDER BY RANDOM() LIMIT 1")
            random_word = c.fetchone()
            if random_word:
                self.root.ids[message_line].text = f'{random_word[0]}'
            else:
                self.root.ids[message_error].text = 'No word in dictionary!'

    def show_word(self, word, column, table):
        with sqlite3.connect('gwords.db') as conn:
            c = conn.cursor()
            c.execute(f"SELECT {column} FROM {table} WHERE {column} =?",
                      (word,))
            new_word = c.fetchone()
            if new_word:
                random_word = f'{new_word[0]}'
                return random_word

    def show_matched_word(self, word, column_a, column_b, table, message_line):
        with sqlite3.connect('gwords.db') as conn:
            c = conn.cursor()
            c.execute(f"SELECT {column_a} FROM {table} WHERE {column_b} =?",
                      (word,))
            new_word = c.fetchone()
            if new_word:
                self.root.ids[message_line].text = f'{new_word[0]}'
                translation = f'{new_word[0]}'
                return translation

    def check_matched_word(self, word, column_a, column_b, table):
        with sqlite3.connect('gwords.db') as conn:
            c = conn.cursor()
            c.execute(f"SELECT {column_a} FROM {table} WHERE {column_b} =?",
                      (word,))
            new_word = c.fetchone()
            if new_word:
                translation = f'{new_word[0]}'
                return translation

    def error_message(self, word, message_error, message_text):
        if not word.strip():
            self.root.ids[message_error].text = message_text
            return True
        return False

    def check_value(self, word, word_2, word_3, message_error, message_text, message_text_1, message_text_2):
        if not word:
            self.root.ids[message_error].text = message_text
            return True
        if not word_2:
            self.root.ids[message_error].text = message_text_1
            return True
        if not word_3:
            self.root.ids[message_error].text = message_text_2
            return True

        if word_2 == word_3:
            self.root.ids[message_error].text = 'Nice!'
        else:
            self.root.ids[message_error].text = 'Wrong!'

    def value_checkboxes(self, value, word, word_2, message_error, message_text, message_text_2):
        if value is True:
            if not word.strip():
                self.root.ids[message_error].text = message_text
                return True
            if word_2:
                word_2.strip()
            else:
                self.root.ids[message_error].text = message_text_2
        else:
            self.clear_checkboxes()
            self.clear_input_messages()


GermanLanguage().run()