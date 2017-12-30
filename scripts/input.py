#coding=utf-8

import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json
import random
from faker import Faker
from jobplus.models import db, User, Company, Job

""" 
#=================================== 职位信息
{
    "id": "pdd",
    "name": "服务端研发工程师",
    "salary_low": "10k",
    "salary_high": "30k",
    "location": "上海",
    "tags": "java",
    "description": "职位描述【岗位职责】移动社交电商平台核心服务研发；海量数据分析处理和挖掘；基础服务和公共组件研发；对现有系统的不足进行分析，找到目前系统的瓶颈，改进系统算法，提高系统性能。职位要求【任职要求】2018年应届毕业生，本科及以上学历，计算机相关专业，热爱计算机科学和互联网技术；2.深刻理解计算机数据结构和算法设计，熟练掌握C/C++、Java或其他一门主流编程语言；3.了解操作系统，数据库和计算机网络原理，有过服务器端应用开发经验；4.优秀的分析问题和解决问题的能力，勇于解决难题；5.强烈的上进心和求知欲，较强的学习能力和沟通能力，具备良好的团队合作精神。【加分项】有编程大赛奖项；有论文专利等；有互联网公司实习经验；具备专业领域的计算机知识和技能的，如搜索引擎、交易系统、数据挖掘/机器学习、云计算、分布式系统等。",
    "raw_description": "<div class=\"fmt\"><h4 class=\"job-detail__heading--catalog\">职位描述</h4><p>【岗位职责】</p><ol><li>移动社交电商平台核心服务研发；</li><li>海量数据分析处理和挖掘；</li><li>基础服务和公共组件研发；</li><li>对现有系统的不足进行分析，找到目前系统的瓶颈，改进系统算法，提高系统性能。</li></ol><h4 class=\"job-detail__heading--catalog\">职位要求</h4><p>【任职要求】</p><ol><li>2018年应届毕业生，本科及以上学历，计算机相关专业，热爱计算机科学和互联网技术；</li></ol><p>2.深刻理解计算机数据结构和算法设计，熟练掌握C/C++、Java或其他一门主流编程语言；<br>3.了解操作系统，数据库和计算机网络原理，有过服务器端应用开发经验；<br>4.优秀的分析问题和解决问题的能力，勇于解决难题；<br>5.强烈的上进心和求知欲，较强的学习能力和沟通能力，具备良好的团队合作精神。</p><p>【加分项】</p><ol><li>有编程大赛奖项；</li><li>有论文专利等；</li><li>有互联网公司实习经验；</li><li>具备专业领域的计算机知识和技能的，如搜索引擎、交易系统、数据挖掘/机器学习、云计算、分布式系统等。</li></ol></div>",
    "company": "上海拼多多",
    "experience_requirement": "经验应届毕业生",
    "degree_requirement": "本科及以上",
    "status": "全职"
  },
  
#======================================== 企业信息
  {
    "id": "varian",
    "name": "瓦里安",
    "logo": "https://sfault-logo.b0.upaiyun.com/157/047/157047563-5a0940b4bc92b_small155",
    "site": "https://www.varian.com",
    "localtion": "北京",
    "description": "大型医疗设备研发与制造",
    "about": "关于我们瓦里安医疗系统公司是全球领先的癌症及其他重大疾病诊断及治疗解决方案的供应商。公司以拯救生命为使命，通过与用户及业界伙伴的紧密合作，每年拯救数十万的生命。瓦里安医疗系统公司致力于提供癌症及其他疾病放射治疗、放射外科、质子治疗和近距离放射治疗设备及相关软件。公司也是全球领先的集医学、科研和工业领域的影像部件及安全检测相关设备的供应商。瓦里安医疗系统公司创立于1948年，是第一家入驻美国加州硅谷的高科技公司。今天，作为美国纽交所上市公司，瓦里安医疗系统公司在美国、欧洲和中国设有生产基地，在全球拥有70多个分支机构。是目前世界上最成功的放疗产品公司。瓦里安进入中国市场已有30多年历史并于2007年在北京经济技术开发区建立中国工厂及地区总部，设立了公司在北美地区以外唯一的直线加速器生产基地。瓦里安医疗系统公司投巨资于2008年在北京设立其亚太地区培训中心。秉承“中国制造为中国”以及“中国制造为世界”的理念，瓦里安医疗系统公司与中国的业界伙伴、医院以及医患群体携手，共同创造一个无惧癌症的世界。公司简介瓦里安医疗系统公司是全球领先的癌症及其他重大疾病诊断及治疗解决方案的供应商。公司以拯救生命为使命，通过与用户及业界伙伴的紧密合作，每年拯救数十万的生命。瓦里安医疗系统公司致力于提供癌症及其他疾病放射治疗、放射外科、质子治疗和近距离放射治疗设备及相关软件。公司也是全球领先的集医学、科研和工业领域的影像部件及安全检测相关设备的供应商。\n\n瓦里安医疗系统公司创立于1948年，是第一家入驻美国加州硅谷的高科技公司。今天，作为美国纽交所上市公司，瓦里安医疗系统公司在美国、欧洲和中国设有生产基地，在全球拥有70多个分支机构。是目前世界上最成功的放疗产品公司。\n\n瓦里安进入中国市场已有30多年历史并于2007年在北京经济技术开发区建立中国工厂及地区总部，设立了公司在北美地区以外唯一的直线加速器生产基地。瓦里安医疗系统公司投巨资于2008年在北京设立其亚太地区培训中心。秉承“中国制造为中国”以及“中国制造为世界”的理念，瓦里安医疗系统公司与中国的业界伙伴、医院以及医患群体携手，共同创造一个无惧癌症的世界。0/1000取消保存",
    "tags": "健康医疗,5001-10000 名雇员,1970 年成立,已上市"
  },

"""

companies_path = os.path.join(os.path.dirname(__file__), "company_1_3.json")
jobs_path = os.path.join(os.path.dirname(__file__), "jobs_1-3.json")

fake = Faker("zh_CN")

class FakerData(object):

    def __init__(self):

        with open(companies_path, "rb") as f:
            self.companies = json.load(f)

        with open(jobs_path, "rb") as f:
            self.jobs = json.load(f)


    def get_job(self, company_id):
        job_list = []
        for item in self.jobs:
            if item["id"] == company_id:
                job_list.append(item)
        return job_list

    def fake_data(self):

        for company in self.companies[:]:
            print(company["name"])
            # 创建企业用户
            c = User(
                username=company["name"],
                email=fake.email(),
                role=User.ROLE_COMPANY
            )
            c.password = "123456"
            db.session.add(c)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                continue

            # 创建企业信息
            d = Company(
                name=company["name"],
                email=c.email,
                logo=company["logo"],
                site=company["site"],
                location=company["localtion"],
                description = company["description"],
                about = company["about"].strip("0/1000取消保存").strip("关于我们"),
                tags=company["tags"]
            )
            d.user_id = c.id
            db.session.add(d)
            db.session.commit()

            # 发布企业职位
            job_list = self.get_job(company["id"])
            for item in job_list:
                job = Job(
                    name=item["name"],
                    salary_low=int(item["salary_low"].strip("k")) * 1000,
                    salary_high=int(item["salary_high"].strip("k")) * 1000,
                    location=item["location"],
                    tags=item["tags"],
                    experience_requirement=item["experience_requirement"],
                    degree_requirement=item["degree_requirement"],
                    description =item["raw_description"]
                )

                job.company_id = d.id

                db.session.add(job)
                db.session.commit()

if __name__ == "__main__":
    f = FakerData()
    f.fake_data()