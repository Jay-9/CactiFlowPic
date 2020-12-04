import re
import os
import time
import pandas
import datetime
import requests
import matplotlib.pyplot as plt


def vlan2id(the_need_vlan):
    if 'vlan' + str(the_need_vlan) in all_vlan:
        return all_vlan['vlan' + str(the_need_vlan)]
    elif str(type(the_need_vlan)) == "<class 're.Match'>":
        if 'vlan' + the_need_vlan.group() in all_vlan:
            return all_vlan['vlan' + str(the_need_vlan.group())]
        else:
            return 'vlan' + the_need_vlan.group()
    else:
        return 'vlan error'


def get_cacti_data():
    graph_start = time.mktime((datetime.datetime.now() + datetime.timedelta(days=-7)).timetuple())
    graph_end = time.mktime((datetime.datetime.now()).timetuple())
    for the_vlan in all_vlan.keys():
        the_url = 'http://10.2.205.55/graph_xport.php?local_graph_id=%d&rra_id=1&view_type=&graph_start=%d&graph_end=%d'\
                  % (eval(vlan2id(the_vlan[4:])), int(graph_start), int(graph_end))
        the_result = requests.post(url=the_url,
                                   data={'action': 'login', 'login_username': 'admin', 'login_password': 'syc@9036idcJk'})\
            .text.replace('"', '')
        with open(the_vlan + '_temp.csv', 'w', encoding='gbk') as f:
            f.write(the_result)
        h24_csv = pandas.read_csv(the_vlan + '_temp.csv', skiprows=9)
        h24_csv.to_csv(the_vlan + '.csv', mode='a', index=False, columns=['Date', 'Inbound', 'Outbound'])
        one_vlan_csv = pandas.read_csv(the_vlan + '.csv')
        one_vlan_csv.drop_duplicates(subset=['Date'], inplace=True)
        err_row = one_vlan_csv[one_vlan_csv['Date'] == 'Date'].index.tolist()
        if len(err_row) != 0:
            one_vlan_csv.drop(index=err_row[0], inplace=True)
        one_vlan_csv.dropna(axis=0, inplace=True)

        date_list = [(datetime.datetime.now() + datetime.timedelta(days=-i)).strftime('%Y-%m-%d') for i in range(15)]
        for one_row in one_vlan_csv.itertuples():
            if one_row.Date.replace('/', '-').split(' ')[0] not in date_list:
                one_vlan_csv.drop(index=one_row.Index, inplace=True)
        one_vlan_csv.reset_index(drop=True, inplace=True)
        one_vlan_csv.to_csv(the_vlan + '.csv', index=False, columns=['Date', 'Inbound', 'Outbound'])
        os.remove(the_vlan + '_temp.csv')


def draw_one_pic(one_vlan):
    today_data = pandas.DataFrame(columns=['Date', 'Inbound', 'Outbound'])
    yesterday_data = pandas.DataFrame(columns=['Date', 'Inbound', 'Outbound'])
    this_week_data = pandas.DataFrame(columns=['Date', 'Inbound', 'Outbound'])
    last_week_data = pandas.DataFrame(columns=['Date', 'Inbound', 'Outbound'])
    this_week_list = [(datetime.datetime.now() + datetime.timedelta(days=-i)).strftime('%Y-%m-%d') for i in range(7)]
    last_week_list = [(datetime.datetime.now() + datetime.timedelta(days=-i)).strftime('%Y-%m-%d') for i in range(7, 14)]
    one_vlan_csv = pandas.read_csv('vlan' + str(one_vlan) + '.csv')  # , converters={'Date': lambda da: da.split(' ')[1][:5]})
    one_vlan_csv['Inbound'] = round(one_vlan_csv['Inbound'] / 1000000000, 2)
    one_vlan_csv['Outbound'] = round(one_vlan_csv['Outbound'] / 1000000000, 2)
    for csv_row in one_vlan_csv.itertuples():
        if csv_row.Date.replace('/', '-').split(' ')[0] in [(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')]:
            yesterday_data = yesterday_data.append(one_vlan_csv.loc[csv_row.Index, :])
        elif csv_row.Date.replace('/', '-').split(' ')[0] in [datetime.datetime.now().strftime('%Y-%m-%d')]:
            today_data = today_data.append(one_vlan_csv.loc[csv_row.Index, :])
    for csv_row in one_vlan_csv.itertuples():
        if csv_row.Date.replace('/', '-').split(' ')[0] in last_week_list:
            last_week_data = last_week_data.append(one_vlan_csv.loc[csv_row.Index, :])
        elif csv_row.Date.replace('/', '-').split(' ')[0] in this_week_list:
            this_week_data = this_week_data.append(one_vlan_csv.loc[csv_row.Index, :])
    yesterday_data.reset_index(drop=True, inplace=True)
    today_data.reset_index(drop=True, inplace=True)
    last_week_data.reset_index(drop=True, inplace=True)
    this_week_data.reset_index(drop=True, inplace=True)
    pic_row = 28
    pic_col = 30
    the_rowspan = 5
    the_colspan = 10
    pic_row_loc = 1
    plt.figure(figsize=(pic_row, pic_col))
    pic1 = plt.subplot2grid((pic_row, pic_col), (pic_row_loc, 0), rowspan=the_rowspan, colspan=the_colspan)  #
    pic1.set_title('Vlan ' + str(one_vlan) + '  real-time')
    for row_today in today_data.itertuples():
        today_data.at[row_today.Index, 'Date'] = today_data.at[row_today.Index, 'Date'].split(' ')[1][:5]
    pic1.plot(today_data['Date'], today_data['Inbound'], label='Inbound')
    pic1.plot(today_data['Date'], today_data['Outbound'], label='Outbound')
    today_inbound_ave = round(today_data['Inbound'].mean(), 2)
    today_inbound_max = round(today_data['Inbound'].max(), 2)
    today_outbound_ave = round(today_data['Outbound'].mean(), 2)
    today_outbound_max = round(today_data['Outbound'].max(), 2)
    pic1.set_xticks([i for i in range(0, len(today_data), 20)])
    pic1.set_xlabel('  Inbound:  Current:' + str(today_data.at[len(today_data)-1, 'Inbound']) + '  Average:' + str(today_inbound_ave) + '  Maximum:' + str(today_inbound_max) + '\n'
               'Outbound:  Current:' + str(today_data.at[len(today_data)-1, 'Outbound']) + '  Average:' + str(today_outbound_ave) + '  Maximum:' + str(today_outbound_max))
    pic1.set_ylabel('Gbits  per  second')
    pic1.legend(loc='best')

    pic2 = plt.subplot2grid((pic_row, pic_col), (pic_row_loc, 11), rowspan=the_rowspan, colspan=the_colspan)  #
    pic2.set_title('Vlan ' + str(one_vlan) + '  Compared with yesterday')
    two_days_Inbound = []
    two_days_Outbound = []
    for row_yesterday in yesterday_data.itertuples():
        yesterday_data.at[row_yesterday.Index, 'Date'] = yesterday_data.at[row_yesterday.Index, 'Date'].split(' ')[1][:5]
    for row_today in today_data.itertuples():
        for row_yesterday in yesterday_data.itertuples():
            if today_data.at[row_today.Index, 'Date'] == yesterday_data.at[row_yesterday.Index, 'Date']:
                two_days_Inbound.append(round(today_data.at[row_today.Index, 'Inbound'] - yesterday_data.at[row_yesterday.Index, 'Inbound'], 2))
                two_days_Outbound.append(round(today_data.at[row_today.Index, 'Outbound'] - yesterday_data.at[row_yesterday.Index, 'Outbound'], 2))
                break
    pic2.plot(today_data['Date'], two_days_Inbound[:len(today_data)], label='Inbound')
    pic2.plot(today_data['Date'], two_days_Outbound[:len(today_data)], label='Outbound')
    pic2.set_xticks([i for i in range(0, len(today_data), 20)])
    pic2.set_xlabel('Today - yesterday   (The same time)')
    pic2.set_ylabel('Gbits')
    pic2.legend(loc='best')

    pic3 = plt.subplot2grid((pic_row, pic_col), (pic_row_loc, 22), rowspan=the_rowspan, colspan=the_colspan)  #
    pic3.set_title('Vlan ' + str(one_vlan) + '  Compared with last week')
    # two_weeks_Inbound = []
    # two_weeks_Outbound = []
    # for row_this_week in this_week_data.itertuples():
    #     this_week_data.at[row_this_week.Index, 'Date'] = this_week_data.at[row_this_week.Index, 'Date'].split(' ')[1][:5]
    # for row_last_week in last_week_data.itertuples():
    #     last_week_data.at[row_last_week.Index, 'Date'] = last_week_data.at[row_last_week.Index, 'Date'].split(' ')[1][:5]
    # for row_this_week in this_week_data.itertuples():
    #     for row_last_week in last_week_data.itertuples():
    #             two_weeks_Inbound.append(round(this_week_data.at[row_this_week.Index, 'Inbound'] - last_week_data.at[row_last_week.Index, 'Inbound'], 2))
    #             two_weeks_Outbound.append(round(this_week_data.at[row_this_week.Index, 'Outbound'] - last_week_data.at[row_last_week.Index, 'Outbound'], 2))
    # pic3.plot(this_week_data['Date'], two_weeks_Inbound[:len(this_week_data)], label='Inbound')
    # pic3.plot(this_week_data['Date'], two_weeks_Outbound[:len(this_week_data)], label='Outbound')
    # pic3.set_xticks([i for i in range(0, len(this_week_data), 200)])
    # pic3.set_xlabel('this week - last week   (The same time)')
    # pic3.set_ylabel('Gbits')
    # pic3.legend(loc='best')

    plt.savefig(r'D:\PyTest\djangoProject\static\pic_today.png')
    # plt.show()


def draw_more_pic(the_expression_id):
    vlan_first = re.match(r'^\d+', the_expression_id)
    vlan_plus = re.findall(r'[+]\d+', the_expression_id)
    vlan_subtraction = re.findall(r'[-]\d+', the_expression_id)


def start_process():
    while True:
        pic_count = input('How many pictures ?')
        for pic_num in range(eval(pic_count)):
            input_vlan_str = input('Pic_%s --> Vlan? or Expression ? : ' % str(pic_num + 1))
            if input_vlan_str.isdigit() or ',' in input_vlan_str:
                vlan_id = vlan2id(input_vlan_str.split(',')) ####################
                if vlan_id == 'vlan error':
                    print('Input vlan%s Error! Please enter again...' % input_vlan_str)
                    break
                else:
                    draw_one_pic(input_vlan_str, vlan_id)  # just one vlan2id ---> 2154
            elif re.match(r'^\d+([+-]\d+)+$', input_vlan_str) is None:
                print('Input Expression Error! Please enter again...')
                break
            else:
                expression_id = re.sub(r'\d+', vlan2id, input_vlan_str)
                if re.match(r'^\d+([+-]\d+)+$', expression_id) is None:
                    print('Input Expression Error or %s Error! Please enter again...' % re.search(r'vlan\d+', expression_id).group())
                    break
                draw_more_pic(expression_id)  # Expression id ---> 2154+2154


all_vlan = {
    'vlan3087': '2159',
    'vlan3027': '2154',
    'vlan3062': '1713',
    'vlan3097': '2160',
    'vlan3037': '2155',
    'vlan3302': '1718',
    'vlan3086': '2158',
    'vlan3056': '2157',
    'vlan3046': '1707',
    'vlan3091': '1717',
    'vlan3016': '2153',
}
# draw_one_pic(['3016', '3027', '3037'])

# while True:
get_cacti_data()
draw_one_pic(3016)
    # time.sleep(300)

# if __name__ == '__main__':  # 1day--5min  1week--30min  1month--2h
# need_vlan = [3027, ]

# if any(key in input_vlan_str for key in calculation_str)
# calculation_str = ('+', '-', '*', '/', '(', ')', )
#         exec('pic_%s=[%s]' % (str(i + 1), input_vlan_str))
#         print(pic_1)
#     break

# TODO ∂‡…Ÿ
