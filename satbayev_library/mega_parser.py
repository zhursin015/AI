import os
import django
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satbayev_library.settings')
django.setup()
from catalog.models import Book


def start_parsing():
    options = webdriver.ChromeOptions()
    # Браузерді көру үшін headless-ті қоспаймыз
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("Satbayev University кітапханасына кіру...")
        driver.get("https://e-lib.satbayev.university/MegaPro/Web/Search/Simple")

        wait = WebDriverWait(driver, 20)

        # 1. Егер батырма iframe ішінде болса, соған ауысамыз
        if len(driver.find_elements(By.TAG_NAME, "iframe")) > 0:
            driver.switch_to.frame(0)
            print("Iframe табылды, ішіне кірдім.")

        # 2. Іздеу батырмасын күту және табу
        print("Батырманы іздеудемін...")
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#SearchButton, input[name='SearchButton'], .search-button")))

        # 3. Батырманы басу (JS арқылы басу сенімдірек)
        driver.execute_script("arguments[0].click();", search_button)
        print("Іздеу басылды!")

        # 4. Нәтижелердің шығуын күту
        time.sleep(10)

        # 5. Мәліметтерді жинау
        print("Деректерді базаға жазу...")
        items = driver.find_elements(By.CLASS_NAME, "itmd_st")  # MegaPro-ның негізгі контейнері

        for item in items[:30]:  # Алғашқы 30 кітап
            try:
                title = item.find_element(By.CLASS_NAME, "Title").text.strip()
                author = item.find_element(By.CLASS_NAME, "Author").text.strip()

                if title:
                    book, created = Book.objects.get_or_create(
                        title=title[:200],
                        author=author[:100],
                        defaults={'summary': "SU ресми сайтынан автоматты түрде алынды."}
                    )
                    if created:
                        print(f"✅ Жаңа: {title[:40]}...")
            except:
                continue

        print("\nЖұмыс аяқталды!")

    except Exception as e:
        print(f"❌ Қате: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    start_parsing()