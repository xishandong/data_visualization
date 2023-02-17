from datetime import datetime


# 计算收益率等信息
def cal_income(value, money):
    total_stock = 0
    total_amount = 0
    for i in range(len(value) - 1):
        total_stock += int(money) / float(value[i])
        total_amount += int(money)
    total = total_stock * float(value[len(value) - 1])
    data = {
        'total': total,
        'total_amount': total_amount,
        'per': '{:.2f}'.format((total / total_amount - 1) * 100)
    }
    return data


# 按照周一到周五进行分离
def different_day_income(data, value):
    monday = {'time': [], 'price': []}
    tuesday = {'time': [], 'price': []}
    wednesday = {'time': [], 'price': []}
    thursday = {'time': [], 'price': []}
    friday = {'time': [], 'price': []}

    for i in range(len(data['time'])):
        dt = datetime.strptime(data['time'][i], '%Y-%m-%d')
        if dt.weekday() == 0:
            monday['time'].append(data['time'][i])
            monday['price'].append(data['price'][i])
        elif dt.weekday() == 1:
            tuesday['time'].append(data['time'][i])
            tuesday['price'].append(data['price'][i])
        elif dt.weekday() == 2:
            wednesday['time'].append(data['time'][i])
            wednesday['price'].append(data['price'][i])
        elif dt.weekday() == 3:
            thursday['time'].append(data['time'][i])
            thursday['price'].append(data['price'][i])
        elif dt.weekday() == 4:
            friday['time'].append(data['time'][i])
            friday['price'].append(data['price'][i])

    mon = cal_income(monday['price'], value)
    tue = cal_income(tuesday['price'], value)
    wed = cal_income(wednesday['price'], value)
    thu = cal_income(thursday['price'], value)
    fri = cal_income(friday['price'], value)

    a = [mon['total'], tue['total'], wed['total'], thu['total'], fri['total']]
    b = [mon['total_amount'], tue['total_amount'], wed['total_amount'], thu['total_amount'], fri['total_amount']]
    c = [mon['per'], tue['per'], wed['per'], thu['per'], fri['per']]

    return {
        'data1': a,
        'data2': b,
        'data3': c
    }



