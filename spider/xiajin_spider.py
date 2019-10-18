# encoding: utf8
import requests
import re
import pymysql
import sys

"""
登录密码是 as
"""
class XiajinSpider:

    def __init__(self, yewu):
        self.username = '371427KHQI'
        self.password = 'cc28ec364be26ea795982a437c716859'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.db = {
            'host': '127.0.0.1',
            'user': 'lyao',
            'password': 'lyao36843',
            'db_name': 'lyao_spider'
        }
        self.cursor = None
        self.db_conn = None
        # self.id_number_list = ['120103198410204224']
        self.id_number_list = []
        self.cookie = {}
        self.sqls = []
        self.yewu = yewu

    def initdb(self):
        """
        从数据库获取待爬取用户身份证号码
        """
        db_conn = pymysql.connect(self.db['host'], self.db['user'], self.db['password'], self.db['db_name'])
        cursor = db_conn.cursor()
        if self.yewu == 'jiguan':
            # 从机关原始表获取身份证号码
            # sql = 'select id_number from jiguan_to_spider where remark = 0 limit 5000'
            sql = 'select id_number from jiguan_to_spider where remark = 0'
        elif self.yewu == 'qiye':
            # 从企业原始表获取身份证号码
            # sql = 'select id_number from qiye_to_spider where remark = 0 limit 500'
            sql = 'select id_number from qiye_to_spider where remark = 0'
        cursor.execute(sql)
        id_numbers = cursor.fetchall()
        for id_number in id_numbers:
            self.id_number_list.append(id_number[0])
        self.cursor = cursor
        self.db_conn = db_conn

    def run(self):
        self.initdb()
        try:
            with requests.session() as fd:
                print(1)
                user_session_uuid = self.get_user_uuid(fd)
                print(2)
                self.get_permission(fd, user_session_uuid)
                grid_session_id = self.get_grid_session_id(fd, user_session_uuid)
                count = 1
                for id_number in self.id_number_list:
                    print('count ======>  {}'.format(count))
                    count += 1
                    tag_session_id = self.get_tag_session_id(fd, user_session_uuid, grid_session_id, id_number)
                    self.select_params_setting(fd, user_session_uuid, grid_session_id, tag_session_id)
                    user_base_info = self.get_user_base_info(fd, user_session_uuid, grid_session_id)
                    if user_base_info:
                        print('user_base_info ==> {}'.format(user_base_info))
                        if self.yewu == 'jiguan':
                            # result = self.get_jiguan_yanglao_data(fd,user_session_uuid,user_base_info)
                            # result = self.get_shiye_yanglao_data(fd,user_session_uuid,user_base_info)
                            # result = self.get_gongshang_yanglao_data(fd,user_session_uuid,user_base_info)
                            result = self.get_gaige_yanglao_data(fd, user_session_uuid, user_base_info)
                            # 更新机关原始数据标记
                            if result:
                                update_sql = 'update jiguan_to_spider set remark = 1 where id_number = "{}"'.format(
                                    id_number)
                            else:
                                update_sql = 'update jiguan_to_spider set remark = 2 where id_number = "{}"'.format(
                                    id_number)
                            self.sqls.append(update_sql)
                        elif self.yewu == 'qiye':
                            # result = self.get_qiye_yanglao_data(fd,user_session_uuid,user_base_info)
                            # result = self.get_shiye_yanglao_data(fd,user_session_uuid,user_base_info)
                            result = self.get_gongshang_yanglao_data(fd, user_session_uuid, user_base_info)
                            # 更新企业原始数据标记
                            if result:
                                update_sql = 'update qiye_to_spider set remark = 1 where id_number = "{}"'.format(
                                    id_number)
                            else:
                                update_sql = 'update qiye_to_spider set remark = 2 where id_number = "{}"'.format(
                                    id_number)
                            self.sqls.append(update_sql)

                        self.save_data()
                    else:
                        continue
        except Exception as e:
            print('exception ==> {}'.format(e))

    def save_data(self):
        for sql in self.sqls:
            # print('sql ==> {}'.format(sql))
            try:
                self.cursor.execute(sql)
            except:
                print('error')
                print('error_sql ==> {}'.format(sql))
        self.sqls = []
        self.db_conn.commit()

    def get_tag_session_id(self, fd, user_session_uuid, grid_session_id, id_number):
        url = 'http://xiajin.ssiid.com/hsu/lov.do'
        data = {
            'method': 'queryPersonBaseInfoByRyidAndXmSi',
            '_random': '0.8439015066000415',
            '__usersession_uuid': user_session_uuid,
            '_laneID': grid_session_id
        }
        _xmlString = '''<?xml version="1.0" encoding="UTF-8"?><p><s shbzhm="''' + id_number + '''"/><s cxbjbjgrybz="1"/></p>'''
        data['_xmlString'] = _xmlString
        headers = self.headers
        response = fd.post(url, data=data, headers=headers)
        return response.text

    def get_grid_session_id(self, fd, user_session_uuid):
        """
        获取用户grid_session_id
        """
        url = 'http://xiajin.ssiid.com/hsu/sijbjptPerOP.do'
        data = {
            'method': 'enterRyxxSi',
            'inputvalue': '',
            '_xmlString': '<?xml version="1.0" encoding="UTF-8"?><p><s biz="37149B"/></p>',
            '_width': 1903,
            '_height': 50,
            '_random': '0.1900018497792706',
            '__usersession_uuid': user_session_uuid
        }
        response = fd.post(url, data=data, headers=self.headers)
        grid_session_id = re.findall('(?<=gridSessionID":").*?(?=")', response.text)[0]
        return grid_session_id

    def get_permission(self, fd, user_session_uuid):
        """
        用户提权操作，不用返回任何数据，请求一下即可
        """
        url = 'http://xiajin.ssiid.com/hsu/SIJBJPTLogon.do'
        data = {
            '_': '1566872544310',
            '__usersession_uuid': user_session_uuid
        }
        response = fd.post(url, data=data, headers=self.cookie)

    def get_user_uuid(self, fd):
        """
        获取用户__usersession_uuid
        """
        url = 'http://xiajin.ssiid.com/hsu/logon.do'
        data = {'method': 'doLogon'}
        _xmlString = '<?xml version="1.0" encoding="UTF-8"?><p><s ybjdlbz="0"/><s userid="371427KHQI"/><s passwd="cc28ec364be26ea795982a437c716859"/><s passWordLogSign="0"/></p>'
        data['_xmlString'] = _xmlString
        response = fd.post(url, data=data, headers=self.headers)

        """
        获取用户cookie信息，并拼接header
        """
        cookie = response.cookies
        BIGipServerhzqrsjz = cookie.get('BIGipServerhzqrsjz')
        JSESSIONID = cookie.get('JSESSIONID')
        loginName = cookie.get('loginName')
        cookie_str = 'loginName=' + loginName + '; yxzgpysb=zitu; yxzgsysb=Canon%20DR-C130%20TWAIN; grywlxzy=ggyw; BIGipServerhzqrsjz=' + BIGipServerhzqrsjz + '; JSESSIONID=' + JSESSIONID
        self.headers['Cookie'] = cookie_str
        # 构建提权需要的cookie
        self.cookie['BIGipServerhzqrsjz'] = BIGipServerhzqrsjz
        self.cookie['JSESSIONID'] = JSESSIONID
        self.cookie['loginName'] = loginName
        return response.json().get('__usersession_uuid')

    def select_params_setting(self, fd, user_session_uuid, grid_session_id, tag_session_id):
        """
        设定用户查询请求参数
        """
        url = 'http://xiajin.ssiid.com/hsu/sgrid.do'
        data = {
            'method': 'fillSGridData',
            '__usersession_uuid': user_session_uuid
        }
        xmlString_first = '<?xml version="1.0" encoding="UTF-8"?><p><s tagsessionid="'
        xmlString_second = '"/><s tagdsname="ds"/><s columnname="Y25scFpBPT0sYzJoaWVtaHQsZUcwPSxjMlo2YUcwPSxZM055Y1E9PSxlbWRzWWc9PSxjbmxrYW14aSxZMko2ZEE9PSxaSGRpYUE9PSxaSGR0WXc9PSxkR0pzWW0xaixhbUpxWjIxag&#61;&#61;"/><s gridSessionID="'
        xmlString_three = '"/><s sumColumnsInfo="[]"/><s selectionMode="single"/><s gridSessionID="'
        xmlString_end = '"/></p>'
        _xmlString = xmlString_first + tag_session_id + xmlString_second + grid_session_id + xmlString_three + grid_session_id + xmlString_end
        data['_xmlString'] = _xmlString
        response = fd.post(url, data=data, headers=self.headers)

    def get_user_base_info(self, fd, user_session_uuid, grid_session_id):
        """
        获取被查询人基本信息
        """
        url = 'http://xiajin.ssiid.com/hsu/sgrid.do?method=virtualScrollView&__usersession_uuid='
        url += user_session_uuid
        data = {
            'gridSessionID': grid_session_id,
            'page': 1,
            'pageSize': 25,
            'updateBeginRowIndex': 0,
            'updateRows': []
        }
        response = fd.post(url=url, data=data, headers=self.headers)
        try:
            return response.json()['rows'][0]
        except:
            return {}

    def get_user_ver_status(self, fd, user_session_uuid, user_base_info):
        """
        待改
        """
        url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        data = {
            'method': 'queryPerAged102PayHis',
            # '_width': 820,
            # '_height': 176,
            '__usersession_uuid': user_session_uuid
        }
        xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s ryid="'
        xmlString_end = '"/><s xzbz="102"/><s jbjgid="37149B03"/></p>'
        ryid = user_base_info['ryid']
        _xmlString = xmlString_head + ryid + xmlString_end
        data['_xmlString'] = _xmlString
        response = fd.post(url, data=data, headers=self.headers)
        print(response.text)
        # grid_session_id = re.findall('(?<=gridSessionID":").*?(?=")',response.text)[0]

    def get_tree_session_id(self, fd, user_session_uuid, user_base_info):
        """
        获取用户菜单树tree_session_id
        """
        url = 'http://xiajin.ssiid.com/hsu/sijbjptPerOP.do'
        data = {
            'method': 'fwdPerOIP',
            '__context_para__': '',
            '_width': 1920,
            '_height': 277,
            '__usersession_uuid': user_session_uuid
        }
        xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s ryid="'
        xmlString_end = '"/></p>'
        ryid = user_base_info['ryid']
        _xmlString = xmlString_head + ryid + xmlString_end
        data['_xmlString'] = _xmlString
        response = fd.post(url, data=data, headers=self.headers)
        tree_session_id = re.findall('(?<=treeSessionId":").*?(?=")', response.text)[0]
        return tree_session_id

    def get_jiguan_yanglao_data(self, fd, user_session_uuid, user_base_info):
        """
        获取机关事业职工养老数据
        """
        """
        表创建语句
        CREATE TABLE `xiajin_jiguan__yanglao_spider_data` (
            `id_number` varchar(255) NOT NULL COMMENT '身份证号码',
            `dwbh` varchar(255) DEFAULT NULL COMMENT '单位编号',
            `cbdwmc` varchar(255) DEFAULT NULL COMMENT '参保单位名称',
            `qsny` varchar(255) DEFAULT NULL COMMENT '起始年月',
            `zzny` varchar(255) DEFAULT NULL COMMENT '终止年月',
            `jfys` varchar(255) DEFAULT NULL COMMENT '缴费月数',
            `jfrq` varchar(255) DEFAULT NULL COMMENT '缴费日期',
            `jflslb` varchar(255) DEFAULT NULL COMMENT '缴费历史类别',
            `fsyytext` varchar(255) DEFAULT NULL COMMENT '发生原因',
            `dwjfjs` varchar(255) DEFAULT NULL COMMENT '单位月缴费基数',
            `dwzjfjs` varchar(255) DEFAULT NULL COMMENT '单位总缴费基数',
            `grjfjs` varchar(255) DEFAULT NULL COMMENT '个人月缴费基数',
            `grzjfjs` varchar(255) DEFAULT NULL COMMENT '个人总缴费基数',
            `dwjfbl` varchar(255) DEFAULT NULL COMMENT '单位缴费比例',
            `grjfbl` varchar(255) DEFAULT NULL COMMENT '个人缴费比例',
            `dwzjfe` varchar(255) DEFAULT NULL COMMENT '单位总缴费额',
            `grzjfe` varchar(255) DEFAULT NULL COMMENT '个人总缴费额',
            `jfehj` varchar(255) DEFAULT NULL COMMENT '缴费合计',
            `bz` varchar(255) DEFAULT NULL COMMENT '备注',
            `dwdjid` varchar(255) DEFAULT NULL COMMENT '单位登记ID',
            `dwyjfe` varchar(255) DEFAULT NULL COMMENT '单位月缴费额',
            `gryjfe` varchar(255) DEFAULT NULL COMMENT '个人月缴费额'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        # 获取新的grid_session_id
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        grid_form_data = {
            'method': 'fwdPerAged102PayHisVAP',
            'ryid': user_base_info['ryid'],
            'xzbz': 102,
            'jbjgid': '37149B03',
            '__context_para__': '',
            '_width': 1675,
            '_height': 383,
            '__usersession_uuid': user_session_uuid
        }
        grid_response = fd.post(url=session_url, data=grid_form_data, headers=self.headers)
        new_grid_session_id = re.findall('(?<=gridSessionID":").*?(?=")', grid_response.text)[0]
        print('new_grid_session_id ==> {}'.format(new_grid_session_id))

        # 获取新的tag_session_id
        tag_form_data = {
            'method': 'queryPerAged102PayHis',
            '__usersession_uuid': user_session_uuid
        }
        xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s ryid="'
        xmlString_end = '"/><s xzbz="102"/><s jbjgid="37149B03"/></p>'
        _xmlString = xmlString_head + user_base_info['ryid'] + xmlString_end
        tag_form_data['_xmlString'] = _xmlString
        tag_response = fd.post(url=session_url, data=tag_form_data, headers=self.headers)
        new_tag_session_id = tag_response.text
        print('tag_session_id ==> {}'.format(new_tag_session_id))

        # 获取用户数据总条数
        msg_count_url = 'http://xiajin.ssiid.com/hsu/sgrid.do'
        msg_count_form_data = {
            'method': 'fillSGridData',
            '__usersession_uuid': user_session_uuid
        }
        msg_xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s tagsessionid="'
        msg_xmlString_center_one = '"/><s tagdsname="dspayhis"/><s columnname="WkhkaWFBPT0sWTJKa2QyMWosY1hOdWVRPT0sZW5wdWVRPT0sYW1aNWN3PT0sWm5OeWNRPT0sYW1ac2MyeGksWm5ONWVRPT0sWkhkcVptcHosWkhkNmFtWnFjdz09LFozSnFabXB6LFozSjZhbVpxY3c9PSxaSGRxWm1KcyxaM0pxWm1KcyxaSGQ2YW1abCxaM0o2YW1abCxhbVpsYUdvPSxZbm89"/><s gridSessionID="'
        msg_xmlString_center_two = '"/><s sumColumnsInfo="[]"/><s selectionMode="single"/><s gridSessionID="'
        msg_xmlString_end = '"/></p>'
        msg_xmlString = msg_xmlString_head + new_tag_session_id + msg_xmlString_center_one + new_grid_session_id + msg_xmlString_center_two + new_grid_session_id + msg_xmlString_end
        msg_count_form_data['_xmlString'] = msg_xmlString
        msg_count_response = fd.post(url=msg_count_url, data=msg_count_form_data, headers=self.headers)
        msg_count = msg_count_response.text
        print('msg_count ===> {}'.format(msg_count))

        # 计算页码
        if int(msg_count) % 25 == 0:
            page_number = int(msg_count) // 25
        else:
            page_number = int(msg_count) // 25 + 1

        # 获取用户机关数据详情
        jiguan_url = 'http://xiajin.ssiid.com/hsu/sgrid.do?method=virtualScrollView&__usersession_uuid='
        post_url = jiguan_url + user_session_uuid
        result = []
        for page in range(1, page_number + 1):
            page_form_data = {
                'gridSessionID': new_grid_session_id,
                'page': page,
                'pageSize': 25,
                'updateBeginRowIndex': 0,
                'updateRows': []
            }
            response = fd.post(url=post_url, data=page_form_data, headers=self.headers)
            data = response.json()['rows']
            result.extend(data)

        id_number = user_base_info['sfzhm']
        for item in result:
            qsny = item['qsny']
            zzny = item['zzny']
            jfrq = item['jfrq']
            item['qsny'] = qsny[:4] + '-' + qsny[4:6] + '-' + qsny[6:8] + ' 00:00:00'
            item['zzny'] = zzny[:4] + '-' + zzny[4:6] + '-' + zzny[6:8] + ' 00:00:00'
            item['jfrq'] = jfrq[:4] + '-' + jfrq[4:6] + '-' + jfrq[6:8] + ' 00:00:00'
            sql = 'insert into xiajin_jiguan_spider_data values ("{}","{}","{}","{}","{}",\
                "{}","{}","{}","{}","{}",\
                "{}","{}","{}","{}","{}",\
                "{}","{}","{}","{}","{}",\
                "{}","{}"\
                )'.format(id_number, item['dwbh'], item['cbdwmc'], item['qsny'], item['zzny'],
                          item['jfys'], item['jfrq'], item['jflslb'], item['fsyytext'], item['dwjfjs'],
                          item['dwzjfjs'], item['grjfjs'], item['grzjfjs'], item['dwjfbl'], item['grjfbl'],
                          item['dwzjfe'], item['grzjfe'], item['jfehj'], item['bz'], item['dwdjid'],
                          item['dwyjfe'], item['gryjfe'])
            self.sqls.append(sql)

    def get_new_grid_session_id(self, fd, user_session_uuid, user_base_info, method, xzbz, jbjgid):
        # 获取新的grid_session_id
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        grid_form_data = {
            'method': method,
            'ryid': user_base_info['ryid'],
            'xzbz': xzbz,
            'jbjgid': jbjgid,
            '__context_para__': '',
            '_width': 1675,
            '_height': 728,
            '__usersession_uuid': user_session_uuid
        }
        if xzbz:
            grid_form_data.pop('xzbz')
        grid_response = fd.post(url=session_url, data=grid_form_data, headers=self.headers)
        new_grid_session_id = re.findall('(?<=gridSessionID":").*?(?=")', grid_response.text)[0]
        return new_grid_session_id

    def get_new_tag_session_id(self, fd, user_session_uuid, user_base_info, method, xzbz, jbjgid):
        # 获取新的tag_session_id
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        tag_form_data = {
            'method': method,
            '__usersession_uuid': user_session_uuid
        }
        xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s ryid="'
        xmlString_end = '"/><s xzbz="{}"/><s jbjgid="{}"/></p>'.format(xzbz, jbjgid)
        _xmlString = xmlString_head + user_base_info['ryid'] + xmlString_end
        tag_form_data['_xmlString'] = _xmlString
        tag_response = fd.post(url=session_url, data=tag_form_data, headers=self.headers)
        new_tag_session_id = tag_response.text
        return new_tag_session_id

    def get_qiye_yanglao_data(self, fd, user_session_uuid, user_base_info):
        """
        获取企业职工养老数据
        """
        """
        表创建语句

        CREATE TABLE `xiajin_qiye_zhigong_yanglao_spider_data` (
            `id_number` varchar(255) NOT NULL COMMENT '身份证号码',
            `dwbh` varchar(255) DEFAULT NULL,
            `cbdwmc` varchar(255) DEFAULT NULL COMMENT '参保单位名称',
            `qsny` varchar(255) DEFAULT NULL COMMENT '起始年月',
            `zzny` varchar(255) DEFAULT NULL COMMENT '终止年月',
            `jfys` varchar(255) DEFAULT NULL,
            `jfrq` varchar(255) DEFAULT NULL COMMENT '缴费日期',
            `jflslb` varchar(255) DEFAULT NULL,
            `fsyytext` varchar(255) DEFAULT NULL COMMENT '发生原因',
            `dwjfjs` varchar(255) DEFAULT NULL COMMENT '单位月缴费基数',
            `dwzjfjs` varchar(255) DEFAULT NULL COMMENT '单位总缴费基数',
            `grjfjs` varchar(255) DEFAULT NULL COMMENT '个人月缴费基数',
            `grzjfjs` varchar(255) DEFAULT NULL COMMENT '个人总缴费基数',
            `dwjfbl` varchar(255) DEFAULT NULL COMMENT '单位缴费比例',
            `grjfbl` varchar(255) DEFAULT NULL COMMENT '个人缴费比例',
            `dwzjfe` varchar(255) DEFAULT NULL COMMENT '单位总缴费额',
            `grzjfe` varchar(255) DEFAULT NULL COMMENT '个人总缴费额',
            `jfehj` varchar(255) DEFAULT NULL COMMENT '缴费合计',
            `bz` varchar(255) DEFAULT NULL COMMENT '备注',
            `dwdjid` varchar(255) DEFAULT NULL,
            `dwyjfe` varchar(255) DEFAULT NULL,
            `gryjfe` varchar(255) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


        """
        yewu = 'qiyezhigong'
        table_name = 'xiajin_qiye_zhigong_spider_data'
        grid_method = 'fwdPerAged101PayHisVAP'
        xzbz = 101
        jbjgid = '37149B01'
        print('grid_method ==> {}'.format(grid_method))
        new_grid_session_id = self.get_new_grid_session_id(fd, user_session_uuid, user_base_info, grid_method, xzbz,
                                                           jbjgid)
        print('new_grid_session_id ==> {}'.format(new_grid_session_id))

        tag_method = 'queryPerAged101PayHis'
        print('tag_method ==> {}'.format(tag_method))
        new_tag_session_id = self.get_new_tag_session_id(fd, user_session_uuid, user_base_info, tag_method, xzbz,
                                                         jbjgid)
        print('new_tag_session_id ==> {}'.format(new_tag_session_id))

        page_number = self.get_page_number(fd, user_session_uuid, new_tag_session_id, new_grid_session_id)
        # print('page_number ==> {}, id_number ==> {}'.format(page_number,user_base_info['sfzhm']))
        if page_number != 0:
            print('page_number ==> {}'.format(page_number))
            self.get_yewu_detail_data(fd, user_session_uuid, new_grid_session_id, table_name, user_base_info, yewu,
                                      page_number)
            return True
        else:
            return False

    def get_shiye_yanglao_data(self, fd, user_session_uuid, user_base_info):
        """
        表创建语句
        CREATE TABLE `xiajin_shiye_spider_data` (
            `id_number` varchar(255) NOT NULL COMMENT '身份证号码',
            `dwbh` varchar(255) DEFAULT NULL COMMENT '单位编号',
            `cbdwmc` varchar(255) DEFAULT NULL COMMENT '参保单位名称',
            `qsny` varchar(255) DEFAULT NULL COMMENT '起始年月',
            `zzny` varchar(255) DEFAULT NULL COMMENT '终止年月',
            `jfys` varchar(255) DEFAULT NULL COMMENT '缴费月数',
            `jfrq` varchar(255) DEFAULT NULL COMMENT '缴费日期',
            `jflslb` varchar(255) DEFAULT NULL COMMENT '缴费历史类别',
            `fsyytext` varchar(255) DEFAULT NULL COMMENT '发生原因',
            `dwjfjs` varchar(255) DEFAULT NULL COMMENT '单位月缴费基数',
            `dwzjfjs` varchar(255) DEFAULT NULL COMMENT '单位总缴费基数',
            `grjfjs` varchar(255) DEFAULT NULL COMMENT '个人月缴费基数',
            `grzjfjs` varchar(255) DEFAULT NULL COMMENT '个人总缴费基数',
            `dwzjfe` varchar(255) DEFAULT NULL COMMENT '单位总缴费额',
            `grzjfe` varchar(255) DEFAULT NULL COMMENT '个人总缴费额',
            `jfehj` varchar(255) DEFAULT NULL COMMENT '缴费合计',
            `bz` varchar(255) DEFAULT NULL COMMENT '备注',
            `dwdjid` varchar(255) DEFAULT NULL COMMENT '单位登记ID',
            `dwyjfe` varchar(255) DEFAULT NULL COMMENT '单位月缴费额'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        # 获取新的grid_session_id
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        table_name = 'xiajin_shiye_spider_data'
        yewu = 'shiye'
        grid_form_data = {
            'method': 'fwdPerLostPayHisVAP',
            'ryid': user_base_info['ryid'],
            'jbjgid': '37149B03',
            '__context_para__': '',
            '_width': 1435,
            '_height': 698,
            '__usersession_uuid': user_session_uuid
        }
        grid_response = fd.post(url=session_url, data=grid_form_data, headers=self.headers)
        new_grid_session_id = re.findall('(?<=gridSessionID":").*?(?=")', grid_response.text)[0]
        print('new_grid_session_id ===> {}'.format(new_grid_session_id))

        # 获取新的tag_session_id
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        tag_form_data = {
            'method': 'queryPerLostPayHis',
            '__usersession_uuid': user_session_uuid
        }
        xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s ryid="'
        xmlString_end = '"/><s jbjgid="37149B03"/></p>'
        _xmlString = xmlString_head + user_base_info['ryid'] + xmlString_end
        tag_form_data['_xmlString'] = _xmlString
        tag_response = fd.post(url=session_url, data=tag_form_data, headers=self.headers)
        new_tag_session_id = tag_response.text
        print('new_tag_session_id ==> {}'.format(new_tag_session_id))

        page_number = self.get_page_number(fd, user_session_uuid, new_tag_session_id, new_grid_session_id)

        if page_number != 0:
            print('page_number ==> {}'.format(page_number))
            self.get_yewu_detail_data(fd, user_session_uuid, new_grid_session_id, table_name, user_base_info, yewu,
                                      page_number)
            return True
        else:
            return False

    def get_gaige_yanglao_data(self, fd, user_session_uuid, user_base_info):
        """
        表创建语句
        CREATE TABLE `xiajin_gaige_spider_data` (
          `id_number` varchar(255) NOT NULL COMMENT '身份证号码',
          `dwbh` varchar(255) DEFAULT NULL,
          `cbdwmc` varchar(255) DEFAULT NULL COMMENT '参保单位名称',
          `qsny` varchar(255) DEFAULT NULL COMMENT '起始年月',
          `zzny` varchar(255) DEFAULT NULL COMMENT '终止年月',
          `jfys` varchar(255) DEFAULT NULL COMMENT '缴费月数',
          `jfrq` varchar(255) DEFAULT NULL COMMENT '缴费日期',
          `jflslb` varchar(255) DEFAULT NULL COMMENT '缴费历史类别',
          `fsyytext` varchar(255) DEFAULT NULL COMMENT '发生原因',
          `dwjfjs` varchar(255) DEFAULT NULL COMMENT '单位月缴费基数',
          `dwzjfjs` varchar(255) DEFAULT NULL COMMENT '单位总缴费基数',
          `grjfjs` varchar(255) DEFAULT NULL COMMENT '个人月缴费基数',
          `grzjfjs` varchar(255) DEFAULT NULL COMMENT '个人总缴费基数',
          `dwjfbl` varchar(255) DEFAULT NULL COMMENT '单位缴费比例',
          `grjfbl` varchar(255) DEFAULT NULL COMMENT '个人缴费比例',
          `dwzjfe` varchar(255) DEFAULT NULL COMMENT '单位总缴费额',
          `grzjfe` varchar(255) DEFAULT NULL COMMENT '个人总缴费额',
          `jfehj` varchar(255) DEFAULT NULL COMMENT '缴费合计',
          `bz` varchar(255) DEFAULT NULL COMMENT '备注'
        ) ENGINE=InnoDB AUTO_INCREMENT=853294 DEFAULT CHARSET=utf8mb4

        """
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        table_name = 'xiajin_gaige_spider_data'
        yewu = 'gaige'
        grid_form_data = {
            'method': 'fwdPerAged109PayHisVAP',
            'ryid': user_base_info['ryid'],
            'xzbz': 109,
            'jbjgid': '37149B03',
            '__context_para__': '',
            '_width': 1435,
            '_height': 698,
            '__usersession_uuid': user_session_uuid
        }

        grid_response = fd.post(url=session_url, data=grid_form_data, headers=self.headers)
        new_grid_session_id = re.findall('(?<=gridSessionID":").*?(?=")', grid_response.text)[0]
        print('new_grid_session_id ===> {}'.format(new_grid_session_id))

        # 获取新的tag_session_id
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        tag_form_data = {
            'method': 'queryPerAged109PayHis',
            '__usersession_uuid': user_session_uuid
        }
        xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s ryid="'
        xmlString_end = '"/><s xzbz="109"/><s jbjgid="37149B03"/></p>'
        _xmlString = xmlString_head + user_base_info['ryid'] + xmlString_end
        tag_form_data['_xmlString'] = _xmlString
        tag_response = fd.post(url=session_url, data=tag_form_data, headers=self.headers)
        new_tag_session_id = tag_response.text
        print('new_tag_session_id ==> {}'.format(new_tag_session_id))

        page_number = self.get_page_number(fd, user_session_uuid, new_tag_session_id, new_grid_session_id)

        if page_number != 0:
            print('page_number ==> {}'.format(page_number))
            self.get_yewu_detail_data(fd, user_session_uuid, new_grid_session_id, table_name, user_base_info, yewu,
                                      page_number)
            return True
        else:
            return False

    def get_gongshang_yanglao_data(self, fd, user_session_uuid, user_base_info):
        """
        表创建语句
        CREATE TABLE `qiye_gongshang_spider_data` (
            `id_number` varchar(255) NOT NULL COMMENT '身份证号码',
            `dwbh` varchar(255) DEFAULT NULL COMMENT '单位编号',
            `cbdwmc` varchar(255) DEFAULT NULL COMMENT '参保单位名称',
            `qsny` varchar(255) DEFAULT NULL COMMENT '起始年月',
            `zzny` varchar(255) DEFAULT NULL COMMENT '终止年月',
            `jfys` varchar(255) DEFAULT NULL COMMENT '缴费月数',
            `jfrq` varchar(255) DEFAULT NULL COMMENT '缴费日期',
            `jflslb` varchar(255) DEFAULT NULL COMMENT '缴费历史类别',
            `fsyytext` varchar(255) DEFAULT NULL COMMENT '发生原因',
            `dwjfjs` varchar(255) DEFAULT NULL COMMENT '单位月缴费基数',
            `dwzjfjs` varchar(255) DEFAULT NULL COMMENT '单位总缴费基数',
            `grjfjs` varchar(255) DEFAULT NULL COMMENT '个人月缴费基数',
            `grzjfjs` varchar(255) DEFAULT NULL COMMENT '个人总缴费基数',
            `dwzjfe` varchar(255) DEFAULT NULL COMMENT '单位总缴费额',
            `grzjfe` varchar(255) DEFAULT NULL COMMENT '个人总缴费额',
            `jfehj` varchar(255) DEFAULT NULL COMMENT '缴费合计',
            `bz` varchar(255) DEFAULT NULL COMMENT '备注',
            `dwdjid` varchar(255) DEFAULT NULL COMMENT '单位登记ID',
            `dwyjfe` varchar(255) DEFAULT NULL COMMENT '单位月缴费额'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        table_name = 'xiajin_gongshang_spider_data'
        yewu = 'gongshang'
        grid_form_data = {
            'method': 'fwdPerHarmPayHisVAP',
            'ryid': user_base_info['ryid'],
            'jbjgid': '37149B03',
            '__context_para__': '',
            '_width': 1435,
            '_height': 698,
            '__usersession_uuid': user_session_uuid
        }

        grid_response = fd.post(url=session_url, data=grid_form_data, headers=self.headers)
        new_grid_session_id = re.findall('(?<=gridSessionID":").*?(?=")', grid_response.text)[0]
        print('new_grid_session_id ===> {}'.format(new_grid_session_id))

        # 获取新的tag_session_id
        session_url = 'http://xiajin.ssiid.com/hsu/perVap.do'
        tag_form_data = {
            'method': 'queryPerHarmPayHis',
            '__usersession_uuid': user_session_uuid
        }
        xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s ryid="'
        xmlString_end = '"/><s jbjgid="37149B03"/></p>'
        _xmlString = xmlString_head + user_base_info['ryid'] + xmlString_end
        tag_form_data['_xmlString'] = _xmlString
        tag_response = fd.post(url=session_url, data=tag_form_data, headers=self.headers)
        new_tag_session_id = tag_response.text
        print('new_tag_session_id ==> {}'.format(new_tag_session_id))

        page_number = self.get_page_number(fd, user_session_uuid, new_tag_session_id, new_grid_session_id)

        if page_number != 0:
            print('page_number ==> {}'.format(page_number))
            self.get_yewu_detail_data(fd, user_session_uuid, new_grid_session_id, table_name, user_base_info, yewu,
                                      page_number)
            return True
        else:
            return False

    def get_yewu_detail_data(self, fd, user_session_uuid, new_grid_session_id, table_name, user_base_info, yewu,
                             page_number):
        # 获取用户业务数据详情
        url = 'http://xiajin.ssiid.com/hsu/sgrid.do?method=virtualScrollView&__usersession_uuid='
        post_url = url + user_session_uuid
        result = []

        for page in range(1, page_number + 1):
            page_form_data = {
                'gridSessionID': new_grid_session_id,
                'page': page,
                'pageSize': 25,
                'updateBeginRowIndex': 0,
                'updateRows': []
            }
            response = fd.post(url=post_url, data=page_form_data, headers=self.headers)
            data = response.json()['rows']
            result.extend(data)

        id_number = user_base_info['sfzhm']
        for item in result:
            qsny = item['qsny']
            zzny = item['zzny']
            jfrq = item['jfrq']
            item['qsny'] = qsny[:4] + '-' + qsny[4:6] + '-' + qsny[6:8] + ' 00:00:00'
            item['zzny'] = zzny[:4] + '-' + zzny[4:6] + '-' + zzny[6:8] + ' 00:00:00'
            item['jfrq'] = jfrq[:4] + '-' + jfrq[4:6] + '-' + jfrq[6:8] + ' 00:00:00'
            if yewu == 'xxx':
                sql = 'insert into xiajin_jiguan_spider_data values ("{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}"\
                    )'.format(id_number, item['dwbh'], item['cbdwmc'], item['qsny'], item['zzny'],
                              item['jfys'], item['jfrq'], item['jflslb'], item['fsyytext'], item['dwjfjs'],
                              item['dwzjfjs'], item['grjfjs'], item['grzjfjs'], item['dwjfbl'], item['grjfbl'],
                              item['dwzjfe'], item['grzjfe'], item['jfehj'], item['bz'], item['dwdjid'],
                              item['dwyjfe'], item['gryjfe'])
            elif yewu == 'qiyezhigong':
                sql = 'insert into {} values ("{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}"\
                    )'.format(table_name, id_number, item['dwbh'], item['cbdwmc'], item['qsny'], item['zzny'],
                              item['jfys'], item['jfrq'], item['jflslb'], item['fsyy'], item['dwjfjs'],
                              item['dwzjfjs'], item['grjfjs'], item['grzjfjs'], item['dwjfbl'], item['grjfbl'],
                              item['dwzjfe'], item['grzjfe'], item['jfehj'], item['bz'], item['dwdjid'],
                              item['dwyjfe'], item['gryjfe'])
            elif yewu == 'shiye' or yewu == 'gongshang':
                sql = 'insert into {} values ("{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}"\
                    )'.format(table_name, id_number, item['dwbh'], item['cbdwmc'], item['qsny'], item['zzny'],
                              item['jfys'], item['jfrq'], item['jflslb'], item['fsyytext'], item['dwjfjs'],
                              item['dwzjfjs'], item['grjfjs'], item['grzjfjs'],
                              item['dwzjfe'], item['grzjfe'], item['jfehj'], item['bz'], item['dwdjid'],
                              item['dwyjfe'])
            elif yewu == 'gaige':
                sql = 'insert into {} values ("{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}","{}",\
                    "{}","{}","{}","{}"\
                    )'.format(table_name, id_number, item['dwbh'], item['cbdwmc'], item['qsny'], item['zzny'],
                              item['jfys'], item['jfrq'], item['jflslb'], item['fsyytext'], item['dwjfjs'],
                              item['dwzjfjs'], item['grjfjs'], item['grzjfjs'], item['dwjfbl'], item['grjfbl'],
                              item['dwzjfe'], item['grzjfe'], item['jfehj'], item['bz'])

            self.sqls.append(sql)

    def get_page_number(self, fd, user_session_uuid, new_tag_session_id, new_grid_session_id):
        # 获取用户数据总条数
        msg_count_url = 'http://xiajin.ssiid.com/hsu/sgrid.do'
        msg_count_form_data = {
            'method': 'fillSGridData',
            '__usersession_uuid': user_session_uuid
        }
        msg_xmlString_head = '<?xml version="1.0" encoding="UTF-8"?><p><s tagsessionid="'
        msg_xmlString_center_one = '"/><s tagdsname="dspayhis"/><s columnname="WkhkaWFBPT0sWTJKa2QyMWosY1hOdWVRPT0sZW5wdWVRPT0sYW1aNWN3PT0sWm5OeWNRPT0sYW1ac2MyeGksWm5ONWVRPT0sWkhkcVptcHosWkhkNmFtWnFjdz09LFozSnFabXB6LFozSjZhbVpxY3c9PSxaSGRxWm1KcyxaM0pxWm1KcyxaSGQ2YW1abCxaM0o2YW1abCxhbVpsYUdvPSxZbm89"/><s gridSessionID="'
        msg_xmlString_center_two = '"/><s sumColumnsInfo="[]"/><s selectionMode="single"/><s gridSessionID="'
        msg_xmlString_end = '"/></p>'
        msg_xmlString = msg_xmlString_head + new_tag_session_id + msg_xmlString_center_one + new_grid_session_id + msg_xmlString_center_two + new_grid_session_id + msg_xmlString_end
        msg_count_form_data['_xmlString'] = msg_xmlString
        msg_count_response = fd.post(url=msg_count_url, data=msg_count_form_data, headers=self.headers)
        msg_count = msg_count_response.text
        print('msg_count ==> {}'.format(msg_count))
        # 计算页码
        if int(msg_count) > 0:
            if int(msg_count) % 25 == 0:
                page_number = int(msg_count) // 25
            else:
                page_number = int(msg_count) // 25 + 1
        else:
            page_number = 0
        return page_number


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: python {} qiye | jiguan'.format(sys.argv[0]))
    xiajinspider = XiajinSpider(sys.argv[1])
    xiajinspider.run()




"""
    CREATE TABLE `xiajin_jiguan__yanglao_spider_data` (
            `id_number` varchar(255) NOT NULL COMMENT '身份证号码',
            `dwbh` varchar(255) DEFAULT NULL COMMENT '单位编号',
            `cbdwmc` varchar(255) DEFAULT NULL COMMENT '参保单位名称',
            `qsny` varchar(255) DEFAULT NULL COMMENT '起始年月',
            `zzny` varchar(255) DEFAULT NULL COMMENT '终止年月',
            `jfys` varchar(255) DEFAULT NULL COMMENT '缴费月数',
            `jfrq` varchar(255) DEFAULT NULL COMMENT '缴费日期',
            `jflslb` varchar(255) DEFAULT NULL COMMENT '缴费历史类别',
            `fsyytext` varchar(255) DEFAULT NULL COMMENT '发生原因',
            `dwjfjs` varchar(255) DEFAULT NULL COMMENT '单位月缴费基数',
            `dwzjfjs` varchar(255) DEFAULT NULL COMMENT '单位总缴费基数',
            `grjfjs` varchar(255) DEFAULT NULL COMMENT '个人月缴费基数',
            `grzjfjs` varchar(255) DEFAULT NULL COMMENT '个人总缴费基数',
            `dwjfbl` varchar(255) DEFAULT NULL COMMENT '单位缴费比例',
            `grjfbl` varchar(255) DEFAULT NULL COMMENT '个人缴费比例',
            `dwzjfe` varchar(255) DEFAULT NULL COMMENT '单位总缴费额',
            `grzjfe` varchar(255) DEFAULT NULL COMMENT '个人总缴费额',
            `jfehj` varchar(255) DEFAULT NULL COMMENT '缴费合计',
            `bz` varchar(255) DEFAULT NULL COMMENT '备注',
            `dwdjid` varchar(255) DEFAULT NULL COMMENT '单位登记ID',
            `dwyjfe` varchar(255) DEFAULT NULL COMMENT '单位月缴费额',
            `gryjfe` varchar(255) DEFAULT NULL COMMENT '个人月缴费额'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
