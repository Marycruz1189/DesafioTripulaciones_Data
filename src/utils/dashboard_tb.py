def filtrar(df, distritos, filtro_distrito, barrios, filtro_barrio, censo, filtro_censo, partido_ant, filtro_partido_ant):

    if filtro_distrito:
        df = df.loc[df['Distritos'].isin(distritos), :]
    
    if filtro_barrio:
        df = df.loc[df['Barrios'].isin(barrios), :]

    if filtro_censo:
        df = df.loc[(df['Censo-2021'] >= censo[0]) & (df['Censo-2021'] <= censo[1]), :]

    if filtro_partido_ant:
        df = df.loc[df['anterior'] == partido_ant, :]

    return df