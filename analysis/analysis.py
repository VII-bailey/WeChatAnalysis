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
import datacompy


class WeChat:
    def __init__(self, room_name):
        self.room_name = room_name

    def sign_in(self):
        try:
            itchat.auto_login(hotReload=True, statusStorageDir='login/login.pkl')
            # itchat.auto_login(enableCmdQR=False)
        except Exception as e:
            print(e)

    def get_room_message(self):
        self.sign_in()
        # 获取全部群
        # print(itchat.get_chatrooms(update=True))

        # 保存到通讯录
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

            else:
                display_name_list = []

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
        # print({'department': department_list, 'name': name_list})
        return {'department': department_list, 'name': name_list}

    def send_info(self):
        # self.sign_in()
        date_str = dt.datetime.now().strftime("%Y%m%d")

        resign_file_dir = os.path.join('result', os.path.join(date_str, 'resign_user.csv'))
        if os.path.exists(resign_file_dir):
            resign_dataframe = pd.read_csv(resign_file_dir, header=0)
        else:
            resign_dataframe = pd.DataFrame()

        onboard_file_dir = os.path.join('result', os.path.join(date_str, 'onboard_user.csv'))
        if os.path.exists(resign_file_dir):
            onboard_dataframe = pd.read_csv(onboard_file_dir, header=0)
        else:
            onboard_dataframe = pd.DataFrame()

        result_str = ''

        if not resign_dataframe.empty:
            for index in resign_dataframe.index:
                result_str += '部门:{0},姓名:{1}\n'.format(resign_dataframe.loc[index]['department'],
                                                       resign_dataframe.loc[index]['name'])
            result_str += '{0}共:{1} 人,\n{2}共:{3} 人,共离职 {4} 人\n'.format(
                (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
                , resign_dataframe.loc[0]['yesterday']
                , dt.datetime.now().strftime("%Y-%m-%d")
                , resign_dataframe.loc[0]['today']
                , resign_dataframe.loc[0]['delta'])

        if not onboard_dataframe.empty:
            for index in onboard_dataframe.index:
                result_str += '部门:{0},姓名:{1}\n'.format(onboard_dataframe.loc[index]['department'],
                                                       onboard_dataframe.loc[index]['name'])
            result_str += '{0}共:{1} 人,\n{2}共:{3} 人,\n共入职 {4} 人\n'.format(
                (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
                , onboard_dataframe.loc[0]['yesterday']
                , dt.datetime.now().strftime("%Y-%m-%d")
                , onboard_dataframe.loc[0]['today']
                , onboard_dataframe.loc[0]['delta'])

        # users = itchat.search_friends(name='用户名称')
        # userName = users[0]['UserName']
        # itchat.send(result_str, toUserName=userName)

        my_room = itchat.search_chatrooms(name='发送信息的群名称')
        room_name = my_room[0]['UserName']

        print(result_str)
        # 发消息
        itchat.send(result_str, toUserName=room_name)


def write_info(user_list_dict):
    date_str = dt.datetime.now().strftime("%Y%m%d")
    file_name = 'info_{}.csv'.format(date_str)
    file_dir = os.path.join('file', file_name)
    if os.path.exists(file_dir):
        os.remove(file_dir)
    data_frame = pd.DataFrame(user_list_dict).drop_duplicates().sort_values(by='department')
    data_frame.to_csv(file_dir, index=False, sep=',')


def compare_csv():
    date_str1 = dt.datetime.now().strftime("%Y%m%d")
    file_dir1 = os.path.join('file', 'info_{}.csv'.format(date_str1))
    file1 = pd.read_csv(file_dir1)

    ate_str2 = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y%m%d")
    # file_dir2 = os.path.join('file', 'info_{}.csv'.format(ate_str2))
    file_dir2 = os.path.join('file', 'info_20210906.csv')
    file2 = pd.read_csv(file_dir2)

    # file_list1 = file1.values.tolist()
    # file_list2 = file2.values.tolist()
    # mask = file2.isin(file1.to_dict(orient='list'))
    # print(mask)
    # result = file2[~mask].dropna()
    # print(result)
    compare = datacompy.Compare(file1, file2, join_columns=['department', 'name'])
    onboard_user = compare.df1_unq_rows
    resign_user = compare.df2_unq_rows

    dir_path = os.path.join('result', date_str1)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    resign_file_dir = os.path.join('result', os.path.join(date_str1, 'resign_user.csv'))
    resign_user['delta'] = len(resign_user)
    resign_user['today'] = len(file1)
    resign_user['yesterday'] = len(file2)
    if os.path.exists(resign_file_dir):
        os.remove(resign_file_dir)
    resign_user.to_csv(resign_file_dir, index=False, sep=',')

    onboard_file_dir = os.path.join('result', os.path.join(date_str1, 'onboard_user.csv'))
    onboard_user['delta'] = len(onboard_user)
    onboard_user['today'] = len(file1)
    onboard_user['yesterday'] = len(file2)
    if os.path.exists(onboard_file_dir):
        os.remove(onboard_file_dir)
    onboard_user.to_csv(onboard_file_dir, index=False, sep=',')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    weChat = WeChat("待分析群名称")
    user_list_dict = weChat.get_user_list()
    write_info(user_list_dict)
    compare_csv()
    weChat.send_info()
