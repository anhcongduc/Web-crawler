from bs4 import BeautifulSoup
import urllib.request
import os
import re
def not_relative_uri(href): # kiểm tra đường link có hợp lệ không
    return re.compile('^http').search(href) is  not  None
def check(link): #kiểm tra link có phải định dạng HTMl để có thể parse không.
    if(len(link)>1):
        if (link[len(link)-4:] != 'html'or link[-10:-5]=='index'):
            return 0
        if (link[len(link) - 7:] == "comment"):
            return 0
        return 1
    return 0
def Get_NewLink(url): # lấy link bài báo tiếp theo có trong trang hiện tại để tiến hành crawl
    #parse HTML để lấy link mới
    start = url.find("//")
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    new_feeds = soup.find(
        'body').find_all(
        'a')
    list_link = []
    new_list_link = []
    #kiểm tra các link bên trong HTML Parse có hợp lệ để crawl không
    for feed in new_feeds:
        link = feed.get('href')
        if (type(link) == type(None)):
            continue
        check_link = not_relative_uri(link)
        if(len(link)<1):
            continue
        if (check_link == 0):
            if (link[0] == "/"):
                link = 'https://' + url[start + 2:] + link
            else:
                link = 'https://' + link
        if (check(link)):
            list_link.append(link)
    for i in range(len(list_link)):
        if (i > 0):
            if (list_link[i - 1] != list_link[i]):
                new_list_link.append(list_link[i])
        else:
            new_list_link.append(list_link[i])

    return new_list_link
def download_image(src,name): # hàm crawl ảnh từ link đã lấy
    fullname = str(name)+".jpg"
    urllib.request.urlretrieve(src,fullname)
def standardizedfile_name(file_name,chr): # lấy tiêu đề của bài báo để đặt tên file TXT sẽ lưu
    while (file_name.find(chr) >-1):
        if(file_name.find(chr)==0):
            file_name=file_name[1:]
            continue
        file_name = file_name[:file_name.find(chr)] + file_name[file_name.find(chr) + 1:]
    return file_name
def Get_Text(url,img_name): # hàm crawl text
    os.chdir('C:/Users/anhco/PycharmProjects/Web Crawler/Text') # thư mục sẽ lưu các file text sẽ lưu
    count = 0
    # tiến hành parse link url
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('body').find('h1')
    if(type(title)==type(None)or len(title.get_text())==0):
        return count
    file_name=title.get_text()
    file_name=standardizedfile_name(file_name,'/')
    file_name=standardizedfile_name(file_name,'"')
    file_name=standardizedfile_name(file_name,'?')
    file_name=standardizedfile_name(file_name,'\t')
    file_name=standardizedfile_name(file_name,'\n')
    file_name=standardizedfile_name(file_name,'\r')
    print(file_name)
    file=open(file_name+".txt","w",encoding="utf-8")
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    file_content=""
    content = soup.find('body').find_all('p')
    for feed in content:
        file_content+=feed.get_text()
    file.write(file_content)
    file.close()
    os.chdir('C:/Users/anhco/PycharmProjects/Web Crawler/Img') #thư mục chưa những ánh sẽ crawl
    Image = soup.find('body').find_all('img') # lấy link các hình ảnh khả dụng trong bài
    ahihi=0
    for img in Image:
        if(ahihi<100):
            src=img.get("src")
            if(src[-3:]!="jpg" and src[-3:]!='png'and src[-3:]!="JPEG"):
                continue
            print(src)
            download_image(src,img_name+count)
            count+=1
            ahihi+=1
        else:
            break
    page.close()
    return count
# hàm main cho đường link vào hàm Get_NewLink
url = Get_NewLink('https://vnexpress.net')
img_name=0# đặt tên các ảnh theo thứ tự 1,2,3,4,-----
flag=0
for i in range(len(url)):
    flag+=1
    print(flag)
    print(url[i])
    count=Get_Text(url[i],img_name)
    img_name+=count
#hiện tại do code này code từ năm ngoái nên bây giờ trang vnexpress.net vẫn có thể crawl text nhưng ảnh thì không crawl được nữa