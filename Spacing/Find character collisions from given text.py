#MenuTitle: Find character collisions from given text
# encoding: utf-8

# Copyright Yanone 2016
# https://yanone.de
# https://github.com/yanone/

# This script goes through a string of text in lower and upper case (a certain language you want to check for collisions) and will detect contour overlaps (collisions) between pairs of glyphs.
# The benefit of this script over going through all possible glyph combinations is efficiency; you’ll only handle collisions that actually show in a certain language.
# In a first round it will detect overlaps merely by adding up the adjoining side bearings and possible kerning,
#   then it will generate a test glyph with the respective paths to see whether they actually collide, to weed out typical overlaps like a TA kerning pair that don’t actually collide (not yet implemented).


text = u'''Lisa del Giocondo là một thành viên trong gia đình Gherardini ở Firenze và Toscana tại Ý. Tên bà được đặt cho hoạ phẩm Mona Lisa, một bức chân dung của bà, do người chồng đặt Leonardo da Vinci vẽ trong thời kỳ Phục hưng Ý. Có rất ít thông tin về cuộc sống của Lisa. Bà sinh ra ở Firenze và kết hôn ở độ tuổi thiếu nữ với một thương gia buôn vải và tơ lụa, người sau này trở thành quan chức địa phương. Bà là mẹ của 6 người con và gia đình thuộc tầng lớp trung lưu có cuộc sống thoải mái, bình lặng. Lisa qua đời sau người chồng nhiều tuổi hơn đáng kể của mình. Vài thế kỷ sau khi Lisa mất, Mona Lisa đã trở thành bức tranh nổi tiếng nhất thế giới và có một số phận tách biệt với người phụ nữ làm mẫu. Các học giả và nhà sưu tầm đã khiến tác phẩm trở thành một biểu tượng toàn cầu và là một đối tượng được thương mại hóa. Đầu thế kỷ 21, một phát hiện của chuyên gia bản thảo thuộc Đại học Heidelberg đã trở thành bằng chứng đủ mạnh để kết thúc những suy đoán về người trong tranh và cuối cùng đã khẳng định được chính Lisa del Giocondo là người ngồi làm mẫu cho bức tranh Mona Lisa. Ngày nay, khoảng 6 triệu người đến tham quan bức tranh mỗi năm tại Bảo tàng Louvre ở Paris, nơi bức tranh trở thành một phần của bộ sưu tập quốc gia Pháp. (xem tiếp…)'''

font = Glyphs.font

collisions = []

for text in [text, text.upper()]:
	for master in font.masters:
		for i in range(len(text) - 1):

			c1 = text[i]
			c2 = text[i + 1]
			g1 = font.glyphs[c1]
			g2 = font.glyphs[c2]

			if g1 and g2:
				if g1.layers[master.id].RSB + g2.layers[master.id].LSB + font.kerningForPair(master.id, g1.rightKerningKey, g2.leftKerningKey) < 0:
					collisions.append((g1.layers[master.id], g2.layers[master.id]))

if collisions:
	tab = font.newTab()

	for collision in collisions:
		tab.layers.append(collision[0])
		tab.layers.append(collision[1])
