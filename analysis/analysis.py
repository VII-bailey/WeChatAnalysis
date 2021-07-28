#!/usr/bin/python3
# -*- coding: utf-8 -*-

# **********************************************************************
# *
# * Author: Rachel
# * Version 1.0.0
# * Date: 2021-07-28 10:29:12
# * Description: 个人项目
# **********************************************************************
import itchat
import os
import datetime as dt
import pandas as pd


class WeChat:
    def __init__(self, room_name):
        self.room_name = room_name

    def sign_in(self):
        try:
            itchat.auto_login(hotReload=True)
            # itchat.auto_login(enableCmdQR=False)
        except Exception as e:
            print(e)

    def get_room_message(self):
        self.sign_in()
        # 获取群
        my_room = itchat.search_chatrooms(name=self.room_name)
        if my_room is None:
            return None
        else:
            return my_room[0]['UserName']

    def get_all_info(self):
        chat_room = itchat.update_chatroom(self.get_room_message(), detailedMember=True)
        return chat_room['MemberList']

    def get_user_list(self):
        # user_list = []
        department_list = []
        name_list = []
        # info_list = []
        display_name_list = []
        chat_room = self.get_all_info()
        for info in chat_room:
            display_name = info['DisplayName']
            if not display_name:
                display_name = info['NickName']

            # info_list.append(display_name)
            if display_name.find('-') != -1:
                display_name_list = display_name.split('-')

            elif display_name.find('~') != -1:
                display_name_list = display_name.split('~')

            elif display_name.find('—') != -1:
                display_name_list = display_name.split('—')

            elif display_name.find('-') != -1:
                display_name_list = display_name.split('-')

            elif display_name.find('－') != -1:
                display_name_list = display_name.split('－')

            elif display_name.find('——') != -1:
                display_name_list = display_name.split('——')

            elif display_name.find('——') != -1:
                display_name_list = display_name.split('——')

            elif display_name.find(' ') != -1:
                display_name_list = display_name.split(' ')

            elif display_name.find('  ') != -1:
                display_name_list = display_name.split('  ')

            elif display_name.find(' ') != -1:
                display_name_list = display_name.split(' ')

            elif display_name.find('～') != -1:
                display_name_list = display_name.split('～')

            if len(display_name_list) == 2:
                department = display_name_list[0].replace(' ', '')
                name = display_name_list[1].replace(' ', '')
            elif len(display_name_list) == 3:
                department = display_name_list[0].replace(' ', '')
                name = display_name_list[2].replace(' ', '')
            else:
                department = ''
                name = display_name

            department_list.append(department)
            name_list.append(name)

        # print('display_name_list=', len(display_name_list))
        # print('department_list=', len(department_list))
        # print('name=', len(name_list))
        # return {'info_list': info_list, 'department': department_list, 'name': name_list}
        return {'department': department_list, 'name': name_list}

    def send_info(self):
        self.sign_in()
        date_str = dt.datetime.now().strftime("%Y%m%d")
        file_dir = os.path.join('result', 'result_{}.csv'.format(date_str))
        dataframe = pd.read_csv(file_dir, header=0)
        result_str = ''
        for index in dataframe.index:
            result_str += '部门:{0},姓名:{1}\n'.format(dataframe.loc[index]['department'], dataframe.loc[index]['name'])
        result_str += '{0}共:{1} 人,{2}共:{3} 人,离职 {4} 人'.format(
            (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
            , dataframe.loc[0]['yesterday']
            , dt.datetime.now().strftime("%Y-%m-%d")
            , dataframe.loc[0]['today']
            , dataframe.loc[0]['delta'])
        # users = itchat.search_friends(name='马传广')
        # userName = users[0]['UserName']
        # itchat.send(result_str, toUserName=userName)
        my_room = itchat.search_chatrooms(name='目标群名称')
        room_name = my_room[0]['UserName']
        # print(result_str)
        itchat.send(result_str, toUserName=room_name)


def write_info(user_list_dict):
    date_str = dt.datetime.now().strftime("%Y%m%d")
    file_name = 'info_{}.csv'.format(date_str)
    file_dir = os.path.join('file', file_name)
    if os.path.exists(file_dir):
        os.remove(file_dir)
    data_frame = pd.DataFrame(user_list_dict)
    data_frame.to_csv(file_dir, index=False, sep=',')


def compare_csv():
    date_str1 = dt.datetime.now().strftime("%Y%m%d")
    file_dir1 = os.path.join('file', 'info_{}.csv'.format(date_str1))
    file1 = pd.read_csv(file_dir1)

    ate_str2 = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y%m%d")
    file_dir2 = os.path.join('file', 'info_{}.csv'.format(ate_str2))
    file2 = pd.read_csv(file_dir2)

    # file_list1 = file1.values.tolist()
    # file_list2 = file2.values.tolist()
    mask = file2.isin(file1.to_dict(orient='list'))
    result = file2[~mask].dropna()

    file_dir = os.path.join('result', 'result_{}.csv'.format(date_str1))
    result['delta'] = len(result)
    result['today'] = len(file1)
    result['yesterday'] = len(file2)
    if os.path.exists(file_dir):
        os.remove(file_dir)
    result.to_csv(file_dir, index=False, sep=',')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    weChat = WeChat("源群名称")
    user_list_dict = weChat.get_user_list()
    write_info(user_list_dict)
    compare_csv()
    weChat.send_info()
