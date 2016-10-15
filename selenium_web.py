from selenium import webdriver

def get_web(url):
      browser = webdriver.PhantomJS( )
      browser.set_window_size(1120, 550)
      browser.get(url)  
      browser.switch_to.frame(browser.find_element_by_xpath("//iframe"))
      web_data = browser.page_source
      browser.quit();
      return web_data
