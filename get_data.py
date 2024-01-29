import pandas as pd
import sqlite3
import folium
from folium.plugins import Search, FeatureGroupSubGroup
from rosreestr2coord import Area



def get_center_from_ppk(cad_num):
    cad_num = cad_num.split(',')[0].strip()
    try:
        area = Area(cad_num)
        coords = area.get_center_xy()[0][0][0]
    except:
        coords = ''
    return float(coords) if coords and coords.isdigit() else None

def get_data_from_table(db_path, name_table):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    table_name = name_table
    query = cursor.execute(f"SELECT * From {table_name}")
    cols = [column[0] for column in query.description]
    data = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

    data['Цвет'] = data['статус'].map({'Выдано': 'green', 'Организуется': 'red', 'В отрисовке': 'blue'})
    data['Иконка'] = data['статус'].map({'Выдано': 'check', 'Организуется': 'car', 'В отрисовке': 'pencil'})

    if data['координаты_участка_x'].isna().any():
        data.loc[data['координаты_участка_x'].isna(), 'координаты_участка_x'] = data.loc[data['координаты_участка_x'].isna(), 'кадастровый_номер'].apply(get_center_from_ppk[1])
        data.loc[data['координаты_участка_y'].isna(), 'координаты_участка_y'] = data.loc[data['координаты_участка_y'].isna(), 'кадастровый_номер'].apply(get_center_from_ppk[0])

    return data
#
# print(list(get_data_from_table('db/survey_db.db','survey')))
# print(get_data_from_table('db/survey_db.db','survey')['Иконка'].unique())


def render_map(df):
    m = folium.Map(location=[df['координаты_участка_x'].mean(), df['координаты_участка_y'].mean()], zoom_start=10)

    layer1 = folium.FeatureGroup(name='Все заказы', show=False)
    m.add_child(layer1)

    cluster_done = FeatureGroupSubGroup(layer1, name="Выдано",control=True)
    m.add_child(cluster_done)
    cluster_began = FeatureGroupSubGroup(layer1, name="Организуется",control=True)
    m.add_child(cluster_began)
    cluster_in_procces = FeatureGroupSubGroup(layer1, name="В отрисовке",control=True)
    m.add_child(cluster_in_procces)


    for index, row in df.iterrows():
        marker = folium.Marker([row['координаты_участка_x'], row['координаты_участка_y']],
                      popup=folium.Popup(
                          "<b>Договор</b> " + row['номер_заявки_договора'] + "<br><b>Вид работ</b> " + row[
                              'вид_работ'] + "<br><b>Дата выезда</b> " + row[
                              'дата_выезда'] + "<br><b>Время выезда</b> " + row[
                              'время_выезда'] + "<br><b>Кадастровый номер</b> " + row[
                              'кадастровый_номер'], max_width=300), name=(row['вид_работ'], row['номер_заявки_договора'], row['кадастровый_номер']),
                                                                                    icon=folium.Icon(color=row['Цвет'], icon=row['Иконка'], prefix='fa'))

        if row['статус'] == 'Выдано':
            cluster_done.add_child(marker)
        elif row['статус'] == 'Организуется':
            cluster_began.add_child(marker)
        elif row['статус'] == 'В отрисовке':
            cluster_in_procces.add_child(marker)

    Search(
        layer=layer1,
        search_label="name",
        geom_type='Point',
        placeholder='Заказы',
        collapsed=False,
        position="topright"
    ).add_to(m)


    folium.LayerControl().add_to(m)

    m.save('statics/map.html')

# render_map(get_data_from_table('db/survey_db.db','survey'))




