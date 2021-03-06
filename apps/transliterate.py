hieroglyphs_dictionary = {'а': '升', 'б': '五', 'в': '归', 'г': '广', 'д': '亼', 'е': '仨', 'ё': '庄',
                          'ж': '川', 'з': '乡', 'и': '仈', 'й': '订', 'к': '片', 'л': '入', 'м': '从', 'н': '廾',
                          'о': '口', 'п': '门', 'р': '户', 'с': '亡', 'т': '丁', 'у': '丫', 'ф': '中', 'х': '乂',
                          'ц': '凵', 'ч': '丩', 'ш': '山', 'щ': '山', 'ъ': '', 'ы': '辷', 'ь': '', 'э': '彐',
                          'ю': '扣', 'я': '牙',

                          'a': '丹', 'b': '乃', 'c': '亡', 'd': '力', 'e': '仨', 'f': '下', 'g': '马', 'h': '卄',
                          'i': '工', 'j': '亅', 'k': '片', 'l': '乚', 'm': '从', 'n': '卜丨', 'o': '口', 'p': '户',
                          'q': '贝', 'r': '尺', 's': '丂', 't': '丁', 'u': '凵', 'v': '', 'w': '山', 'x': '乂',
                          'y': '丫', 'z': '乙'}  # Найти символ для V

passport_dictionary = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
                       'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
                       'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
                       'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'ъ': 'ie', 'э': 'e', 'ю': 'iu',
                       'я': 'ia'}


class Transliterate:
    def __init__(self):
        pass

    def transliterate_hieroglyphs(self):
        for key in hieroglyphs_dictionary:  # Циклически заменяем все буквы в строке
            self = self.lower().replace(key, hieroglyphs_dictionary[key])
        return self

    def transliterate_passport(self):
        for key in passport_dictionary:  # Циклически заменяем все буквы в строке
            self = self.lower().replace(key, passport_dictionary[key]).upper()
        return self


'''
А –   丹升什闩
Б –   石右五
В –   归乃巧日扫丑
Е –   巨乞仨巳它正臣亖乜
Ж –   水卌兴川氽米
З –   乡弓
Й –   订计认
К –   片长
Л –   几人穴入
М –   从册爪
Н –   廾卄
П –   冂门刀
Р –   卩户尸
С –   匚仁亡
Т –   丁丅
Э –   彐刁当
Ю –    扣仰
Я –   牙兑兄只

A –   丹升什闩
B –   归乃巧日扫丑
C –   匚仁亡
E –   巨乞仨巳它正臣
F –   下彳
G –   呂马
H –   廾卄
I –   丨工
K –   片长
L –   乚心
M –   从册
N –   卜丨  — найти одним символом
O –   口囗
P –   户尸
R –   尺夬只艮
S –   丂与
V
W –   山屮
'''
