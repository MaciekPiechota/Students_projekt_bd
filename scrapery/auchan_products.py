import requests
from product import *

ENRG_URL = "https://zakupy.auchan.pl/api/v2/products?categoryId=13264&itemsPerPage=200&page=1&subCategoryId=13273"
PIZZA_URL = "https://zakupy.auchan.pl/api/v2/products?categoryId=18392&itemsPerPage=200&page=1"
PIWO_URL = "https://zakupy.auchan.pl/api/v2/products?categoryId=18697&itemsPerPage=200&page=1"
PIWO_MOCNE_URL = "https://zakupy.auchan.pl/api/v2/products?categoryId=18766&itemsPerPage=200&page=1"
PIWO_SMAKOWE_URL = "https://zakupy.auchan.pl/api/v2/products?categoryId=18706&itemsPerPage=200&page=1"
PIWO_PSZEN_URL = "https://zakupy.auchan.pl/api/v2/products?categoryId=18703&itemsPerPage=200&page=1"
PIWO_CIEMNE_URL = "https://zakupy.auchan.pl/api/v2/products?categoryId=18700&itemsPerPage=200&page=1"
PIWO_REG_URL = "https://zakupy.auchan.pl/api/v2/products?categoryId=18694&itemsPerPage=200&page=1"

PIWO = [PIWO_URL, PIWO_MOCNE_URL, PIWO_SMAKOWE_URL,
        PIWO_PSZEN_URL, PIWO_CIEMNE_URL, PIWO_REG_URL]
ENRG = [ENRG_URL]
PIZZA = [PIZZA_URL]

# dla piwa
# authorization (możliwe że tego nie trzeba) i PHPSESSID trzeba zmieniać
# https://zakupy.auchan.pl/shop/piwo-wino-alkohole/piwo-cydr/piwa-jasne-pilsner.c-18697?qq=%7B%7D
# zalogować się -> F12 -> F5 -> products?... (copy as fetch Node.js)


def scrape_auchan(what):
    if what == "PIWO":
        urls = PIWO
        t = Type.PIWO
    elif what == "PIZZA":
        urls = PIZZA
        t = Type.PIZZA
    else:
        urls = ENRG
        t = Type.ENERGY

    products = []

    for url in urls:
        r = requests.get(url,
                         headers={
                             "accept": "application/json",
                             "accept-language": "pl",
                             "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMWMyZWQ3N2QyYTQ3YWM4YTAxZDc4MDMwZWFhMWEyYyIsImp0aSI6ImMyOTFjMzVlMmM1NjUxYTg0ZjliYjg0NjlmN2VmYTU3MmI3NWIxZjRiOTc4YzE3NTI0ZGE5M2IyNTM1YWE2ZWE5NDVhZTVhYWNmZjFhZGZkIiwiaWF0IjoxNjQzMDY1NDkxLjc4MjQ2LCJuYmYiOjE2NDMwNjU0OTEuNzgyNDY0LCJleHAiOjE2NDMxNTE4OTEuNzU0NDI1LCJzdWIiOiI2NzU3NjgiLCJzY29wZXMiOltdfQ.B-gMPfpMpzIQgr0Ke9a3UKg_RUYH3FBHBiLGUkg9sxqeon7ALV8IaKIvJpViM138HISmkPXxuCR046paETPg80I6aq_eya4_wELGx8Gv13c2aRyv9dl0Q9EF90pu8oMBaPIi1qNbd_D2wXcmftjtlWwgq15KYYzHgnH2KCPIYBJCWOzrXwWyEyQCdMqbT4GdQkhPLgKc4MmMu2dDFlAPKhl8a6UN7igr_L2a55okVFvzyAH6uazONm146ReQMBFm5MrMpZmdpsmOY2EkECqb6U-xFhZkULjCImTfdsTNhTNyGLfJPChR-Z5QEAaGWK0UxHo1CNnYLV7xwgE03dzMQA",
                             "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
                             "sec-ch-ua-mobile": "?0",
                             "sec-ch-ua-platform": "\"Linux\"",
                             "sec-fetch-dest": "empty",
                             "sec-fetch-mode": "cors",
                             "sec-fetch-site": "same-origin",
                             "cookie": "token_type=Bearer; PHPSESSID=3db39fc5b85e1a4680b471674863a532; _gcl_aw=GCL.1643053785.Cj0KCQiAubmPBhCyARIsAJWNpiM6mVA2daLADiXJlAONj0xNv5u-NpgWo6xSiBkIej0ds6ztBJzXsOIaAiXtEALw_wcB; _gcl_au=1.1.1402512686.1643053785; startup_popup_closed=true; OptanonAlertBoxClosed=2022-01-24T19:50:18.616Z; _gid=GA1.2.2042990619.1643053819; _gac_UA-12168540-9=1.1643053819.Cj0KCQiAubmPBhCyARIsAJWNpiM6mVA2daLADiXJlAONj0xNv5u-NpgWo6xSiBkIej0ds6ztBJzXsOIaAiXtEALw_wcB; _gac_UA-12168540-5=1.1643053835.Cj0KCQiAubmPBhCyARIsAJWNpiM6mVA2daLADiXJlAONj0xNv5u-NpgWo6xSiBkIej0ds6ztBJzXsOIaAiXtEALw_wcB; _hjSessionUser_2533132=eyJpZCI6IjExYjRhYWM4LWU3YzYtNTEzYi1iYmZmLWIzNGQzYzczMDAwYiIsImNyZWF0ZWQiOjE2NDMwNTM3ODU0MDYsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_2533132=eyJpZCI6IjAwZjkxMGI5LTU3YmMtNGRjMy04ZDkxLTA1YmM3YzIwMzk1MiIsImNyZWF0ZWQiOjE2NDMwNjUwNTYzNzQsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _ga_88WZ9X400Y=GS1.1.1643065460.1.0.1643065460.0; OptanonAlertBoxClosed=2022-01-24T23:04:25.083Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jan+25+2022+00%3A04%3A25+GMT%2B0100+(czas+%C5%9Brodkowoeuropejski+standardowy)&version=6.21.0&isIABGlobal=false&hosts=&consentId=016507f5-6ad8-499b-b721-58f8ebd56359&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; _gat_UA-12168540-1=1; _gat_UA-12168540-5=1; _ga_4FX6Q178DX=GS1.1.1643065359.1.1.1643065488.0; _gat_UA-12168540-9=1; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMWMyZWQ3N2QyYTQ3YWM4YTAxZDc4MDMwZWFhMWEyYyIsImp0aSI6ImMyOTFjMzVlMmM1NjUxYTg0ZjliYjg0NjlmN2VmYTU3MmI3NWIxZjRiOTc4YzE3NTI0ZGE5M2IyNTM1YWE2ZWE5NDVhZTVhYWNmZjFhZGZkIiwiaWF0IjoxNjQzMDY1NDkxLjc4MjQ2LCJuYmYiOjE2NDMwNjU0OTEuNzgyNDY0LCJleHAiOjE2NDMxNTE4OTEuNzU0NDI1LCJzdWIiOiI2NzU3NjgiLCJzY29wZXMiOltdfQ.B-gMPfpMpzIQgr0Ke9a3UKg_RUYH3FBHBiLGUkg9sxqeon7ALV8IaKIvJpViM138HISmkPXxuCR046paETPg80I6aq_eya4_wELGx8Gv13c2aRyv9dl0Q9EF90pu8oMBaPIi1qNbd_D2wXcmftjtlWwgq15KYYzHgnH2KCPIYBJCWOzrXwWyEyQCdMqbT4GdQkhPLgKc4MmMu2dDFlAPKhl8a6UN7igr_L2a55okVFvzyAH6uazONm146ReQMBFm5MrMpZmdpsmOY2EkECqb6U-xFhZkULjCImTfdsTNhTNyGLfJPChR-Z5QEAaGWK0UxHo1CNnYLV7xwgE03dzMQA; refresh_token=def50200b0a7222002260524bee81c3d3459f6f07966754af2513a5eeac8730b39e210a53f000f0f2ab98f02bccbf4d3daea2598177ad27484122ce4640606943e8e407b12fc859726e2428cf2c9c5559395616fa1c659de1839bbc91cd2d923e9606057d9730b1c65d5916940a53613c6a7ec9d252b2eae2a77dadec5e406c51ce0e6fee8112116217dfd29bfe61a78fda253eb29dec4cc865c9691ab83459619cca9b7c261b960736c2560874084feddf751f0bdd115213c040ad83cd94909ace7dfb687d7bcb00a2f043694f74e4b7527e57d1e2dc3f24a5b5b6388bb3de40e6d2488fc0d4a08ce767589ecdc12f51d803a6ddafef59be137b35c76ebfd58a646ffd5a1a86587883b0d51b9cb42a23b438ef263889d62b94bae6ed3e6ba6e3337106b9ed7d3aa266dde07ed3de3eda3df6a2876bcffa9762b8dd24f91cd28ab2f5b86113f2dc9ba806fea6aa18ff843238829890ebffa732b42d026242c1f1c0fb0cc255775370db443f31390e1ad871d02e14ba49528943c821581d8cc47160f19edf2f57b; _ga=GA1.2.1498697593.1643053819; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jan+25+2022+00%3A05%3A08+GMT%2B0100+(czas+%C5%9Brodkowoeuropejski+standardowy)&version=6.25.0&isIABGlobal=false&hosts=&consentId=016507f5-6ad8-499b-b721-58f8ebd56359&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; _ga_YQ1M2YKEZQ=GS1.1.1643064867.3.1.1643065516.19; _ga_WT27NKQFH5=GS1.1.1643064867.3.1.1643065516.0",
                             "Referrer-Policy": "strict-origin-when-cross-origin"
                         })
        results = r.json()["results"]

        for result in results:
            result_data = result["defaultVariant"]
            name = result_data["name"]
            price_data = result_data["price"]
            discount = price_data["isDiscounted"]
            price = float(price_data["grossDiscounted"])
            amount_data = result_data["packageInfo"]
            amount = convert_unit(
                float(amount_data["packageSize"]), amount_data["packageUnit"])

            products.append(Product(t, name, price, amount, discount))

    return products
