import requests

# بيانات تطبيقك من Cryptohopper Developer Console
client_id = '[9gZgRFZrzj5hh4y0tfNzs1gaozVYNl8BSBEhtNyDiyjevUOQv21QmGBrsCcEgvZQ]'
client_secret = '[m719DnC6BjTYNaOhBEHJURe2RGMFQeigrakQjyOfL6UfPmKh6Sjs87BhWcXVwFbp]'
redirect_uri = 'http://localhost/'

# قناة تيليجرام
bot_token = '7974713193:AAGaE-sjvB7kTAt_yg6Mp68_xE5lC_czdA8'
channel_id = '@Cryptoships95'

# الصلاحيات المطلوبة
scope = 'read,notifications,manage,trade'

# رابط التفويض
authorize_url = 'https://www.cryptohopper.com/oauth2/authorize'
code_uri = f'{authorize_url}?client_id={client_id}&response_type=code&scope={scope}&state=any&redirect_uri={redirect_uri}'

# ✳️ الخطوة دي للمعلومة فقط، متتوقعش إنها تفتح المتصفح تلقائي
print("افتح الرابط ده في المتصفح وسجل دخولك:")
print(code_uri)

# ✅ بعد ما تفتح الرابط في المتصفح وتوافق، هيرجعك إلى redirect_uri ومعاه الكود
# مثال: http://localhost/?code=123456789
# انسخ الكود وضعه هنا
code = '123456789'
