import base64

with open(r'd:\Html Files\1000078800.webp', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')

data_uri = 'data:image/webp;base64,' + b64

with open(r'd:\Html Files\Visiting card 1.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Current img src found:", 'src="D:\\Html Files\\1000078800.webp"' in html)
print("Alt src found:", 'src="1000078800.webp"' in html)

# Replace both possible forms
new_html = html.replace('src="D:\\Html Files\\1000078800.webp"', 'src="' + data_uri + '"')
new_html = new_html.replace("src=\"D:\\Html Files\\1000078800.webp\"", 'src="' + data_uri + '"')

with open(r'd:\Html Files\Visiting card 1.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

if 'data:image/webp;base64,' in new_html:
    print('SUCCESS: Image embedded as Base64!')
else:
    print('FAILED')

import os
size = os.path.getsize(r'd:\Html Files\Visiting card 1.html')
print(f'File size: {size} bytes ({size/1024/1024:.2f} MB)')
