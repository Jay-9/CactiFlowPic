import re
import matplotlib
import datetime
import pandas
import requests
import matplotlib.pyplot as plt

x = '3016,3027,3037'
y = x.split(',')
pic_row = 28 * len(y)
pic_col = 30
plt.figure(figsize=(pic_row, pic_col))
the_rowspan = 5
the_colspan = 10
for yind, yval in enumerate(y):
    print(yind, '-->', yval)
    pic_row_loc = yind * 28
    print(pic_row_loc)
    pic1_1 = plt.subplot2grid((pic_row, pic_col), (pic_row_loc, 0), rowspan=the_rowspan, colspan=the_colspan)  #
    pic1_1.set_title('Vlan ' + str(yval) + '  real-time')
    plt.show()
# exec('pic_%s=[%s]' % (str(i + 1), 3))

#
# plt.figure(figsize=(30, 30))
# ax1 = plt.subplot2grid((30, 10), (23, 0), rowspan=10, colspan=11)
# font_title = matplotlib.font_manager.FontProperties(fname=r'/jay/the_font.ttf', size=20)
# font_week = matplotlib.font_manager.FontProperties(fname=r'/jay/the_font.ttf', size=10)
# font_num = matplotlib.font_manager.FontProperties(fname=r'/jay/the_font.ttf', size=8)
#
# # ax1.set_xlabel("日       期", fontproperties = font_title)
# ax1.set_ylabel("流       量", fontproperties=font_title)
# ax1.set_title("流    量    统    计    图\n", fontproperties=font_title)
# ax1.set_ylim([0, max(total_flow) + 50])
# ax1.set_xticks([])
#
# legend_ck = ax1.bar(x_lab, ck_flow, color=['#FF7648'], align='center')
# legend_hl = ax1.bar(x_lab, hl_flow, color=['#8FD9F8'], bottom=ck_flow, align='center')
# legend_idc = ax1.bar(x_lab, idc_flow, color=['#DDEFBF'], bottom=hl_flow, align='center')
# ax1.set_xticks(range(0, 30))
#
# # ax1.spines['bottom'].set_color('r')
# ax1.spines['left'].set_position(('data', -1.5))
# ax1.spines['right'].set_color('none')
# ax1.spines['top'].set_color('none')
#
# for xx, yy, zz in zip(x_lab, ck_flow, ck_per):
#     ax1.text(xx, 10, str(yy) + 'G\n' + str(zz) + '%', ha='center', fontsize=7)
# for xx, yy, zz in zip(x_lab, hl_flow, hl_per):
#     ax1.text(xx, max(ck_flow)+5, str(yy) + 'G\n' + str(zz) + '%', ha='center', fontsize=7)
# for xx, yy, zz in zip(x_lab, idc_flow, idc_per):
#     ax1.text(xx, max(ck_flow+hl_flow) + 5, str(yy) + 'G\n' + str(zz) + '%', ha='center', fontsize=7)
# for xx, yy, zz in zip(x_lab, nwl_per, total_flow):
#     ax1.text(xx, max(total_flow)-60, '总流量\n' + str(zz) + 'G\n\n' + '内网率\n' + str(yy) + '%', ha='center',
#              fontproperties=font_num)
# for xx, yy, zz in zip(x_lab, all_user, average_bandwidth):
#     ax1.text(xx, max(ck_flow+hl_flow)+260, '总用户数\n' + str(yy) + '\n'*4 +
#              '户均带宽\n' + str(zz) + '\nKbps/户', ha='center', fontproperties=font_num)
# for xx in x_lab:
#     ax1.text(xx, -90, xx.split('\n')[0] + '\n' + xx.split('\n')[1][:5], ha='center', fontsize=9)
#
# week_dic = {'0': '日', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六'}
# for xx in x_lab:
#     the_num = datetime.datetime(year=2020,
#                             month=int(xx.split('\n')[0].replace('-', ',').replace('/', ',').split(',')[0]),
#                             day=int(xx.split('\n')[0].replace('-', ',').replace('/', ',').split(',')[1]))\
#         .strftime('%w')
#     ax1.text(xx, max(ck_flow+hl_flow)+120, week_dic[the_num], ha='center', fontproperties=font_week)
#
# ax2 = plt.subplot2grid((30, 10), (19, 0), colspan=1, rowspan=2)
# ax2.legend(handles=[legend_idc, legend_hl, legend_ck], labels=["I D C", "互联互通", "出    口"], loc=2, prop=font_title)
# ax2.axis('off')
#
# ax3 = ax1.twinx()
# ax3.spines['left'].set_color('none')
# ax3.spines['right'].set_position(('data', -1.5))
# ax3.spines['top'].set_color('none')
# ax3.plot(x_lab, nwl_per, color='r', linewidth=1)
# ax3.set_ylim([70, 98])
# ax3.set_xticks([])
# ax1.set_xticks([])

