import get_fb_data as cs

if __name__ == '__main__':

    # username = 'nishasingh270492@gmail.com'
    # passwd = 'popjohn92'
    
    fp = open("credentials.txt","rU")
    lines = fp.readlines()
    fp.close()
    
    fp = open("user_search_info.txt", "rU")
    user_details = fp.readlines()
    fp.close()
    
    try:
        username = lines[0].strip()
        passwd = lines[1].strip()
        user_search_info = [detail.strip() for detail in user_details]
    except:
        print "Check the credentials file."
    
    cs.fetch_fb_details(user_search_info, username, passwd)