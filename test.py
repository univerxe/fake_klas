import requests


def get_course_taken(cookies: str, headers: dict) -> dict:
    course_taken_response = requests.post('https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreSungjukInfo.do', cookies=cookies, headers=headers)
    
    taken_subjects = []
    
    course_taken = course_taken_response.json() 
    for semester in course_taken:
        for subject in semester["sungjukList"]:
            taken_subjects.append(subject["gwamokKname"])
            
    return set(taken_subjects)
   
    
def get_course_before_after(headers: dict, major_sub: set) -> dict:
    data_bef_aft = {
        'opcode': '700',
        'mrd_path': 'TYv%ce%07w%26j%f1%f3%f5%f7%08%f6%f4%f2HL%87%15%80%2f%91u%a7%bb%01%0f%90%d9%c8f%8a%dbn%a5%99%d7%7ed%1d%a7%bb%3c%b6%cdS%d4%60%5e%5e%3d0%a1%d3%d0G%88%8dx%ce%afRC%5b%0f%a3%f9%e6%ff%5b%99%137OE%5d%7d%dc%b2%2b%d7%8bF%5c%ab%00x%07%d0%19T%f7%cf%dd%e0%04%05%ea%09%c9%7b%2d%05%08%84%01%96%d3m%9b%1a',
        'mrd_param': '9%17%3b%11%88%9b%b6%db%f1%f3%f5%f7%08%f6%f4%f2%a5%2dDU%3d%bb%40%a4qY%bfo%fe%97%5e%dc%eaN%c8%ba%9f%12%de%b8r%e5%92%e6%d3%5dU%a2%05%1d%9a%9c%03%1d%f1%ad%e8%5e%1a%c5U%82%3b%d7R%09%ad%fe%ca%a3%c9z%db%be%16%89%8aY%1e%a0%d0%90%3d%88%e6%ef03%ef1%d5zA%cah%2fS%c2%ab%94%87%e6%c9%e3M%b22%efy%dfL%b3',
        'mrd_plain_param': '',
        'mrd_data': '',
        'runtime_param': '',
        'mmlVersion': '0',
        'protocol': 'sync',
        'enc_type': '11',
    }

    response_bef_aft = requests.post('https://report.kw.ac.kr:8585/ReportingServer/service', headers=headers, data=data_bef_aft)
    xml_data = response_bef_aft.text
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_data)

    course_list = []

    for tl in root.findall('.//BODY/PG/TL'):
        course_text = tl.text
        course_list.append(course_text)
        
    course_pairs = [(course_list[i - 1], course_list[i + 1]) for i, item in enumerate(course_list) if item == '▶']

    before_list = []
    after_list = []

    for before, after in course_pairs:
        before_list.append(before)
        after_list.append(after)
        
    return {"before": [(name,"false") if name not in major_sub else (name, "true") for name in before_list], "after": [(name,"false") if name not in major_sub else (name, "true") for name in after_list]}


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s - %(levelname)s', filename='test.log', encoding='utf-8')
    logging.info("Start program")
    
    cookies = {
        'SESSION': '',
    }
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://klas.kw.ac.kr',
        'Referer': 'https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreStdPage.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    major_sub = get_course_taken(cookies, headers)
    result = get_course_before_after(headers, major_sub)
    
    logging.debug(len(result["before"]) == len(result["after"]))
    logging.debug(result)
    
    logging.info("End program")