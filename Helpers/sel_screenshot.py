def capture_screenshot(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from PIL import Image
    from io import BytesIO
    import time

    # Set up Chrome WebDriver
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL to capture
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")

    # Viewport height
    viewport_height = driver.execute_script("return window.innerHeight")
    driver.set_window_size(1920, viewport_height)  # Adjust the width as needed

    # Scroll and capture the entire page
    images = []
    for y in range(0, total_height, viewport_height):
        driver.execute_script(f"window.scrollTo(0, {y})")
        time.sleep(0.5)  # Small delay for page to stabilize
        img = Image.open(BytesIO(driver.get_screenshot_as_png()))
        images.append(img)

    # Stitch images together
    total_width = images[0].width
    stitched_image = Image.new('RGB', (total_width, total_height))
    offset = 0
    for img in images:
        stitched_image.paste(img, (0, offset))
        offset += img.height

    stitched_image.save('complete_webpage_screenshot.png')
    driver.quit()
    return stitched_image
