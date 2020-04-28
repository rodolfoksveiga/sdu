import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

charateristics_table = """ CREATE TABLE IF NOT EXISTS Caracteristicas (
						   tipologia_c       VARCHAR(4)  NOT NULL,
						   id_caso_c         VARCHAR(7)  NOT NULL,
						   ambiente_c        VARCHAR(10) NOT NULL,
						   amb               SMALLINT,
						   u_par_ext         FLOAT(3),
						   ct_par_ext        FLOAT(2),
						   exp_cob           SMALLINT,
						   u_cob             FLOAT(2),
						   ct_cob		     SMALLINT,
						   exp_pis           SMALLINT,
						   u_pis_ext         FLOAT(2),
						   ct_pis_ext        SMALLINT,
						   u_vid             FLOAT(2),
						   f_svid            FLOAT(2),
						   fat_ven           FLOAT(2),
						   abs_par           FLOAT(2),
						   abs_cob           FLOAT(2),
						   u_par_int         FLOAT(2),
						   ct_par_int        SMALLINT,
						   somb              SMALLINT,
						   vent_cruz         SMALLINT,
						   area_util         FLOAT(2),
						   a_par_int         FLOAT(2),
						   par_ext_n         FLOAT(2),
						   par_ext_s         FLOAT(2),
						   par_ext_l         FLOAT(2),
						   par_ext_o         FLOAT(2),
						   av_ao_n           FLOAT(2),
						   av_ao_s           FLOAT(2),
						   av_ao_l           FLOAT(2),
						   av_ao_o           FLOAT(2),
						   anual_a           FLOAT(12),
						   anual_R           FLOAT(12),
						   Hdesconf          REAL,
						   horario           TIME,
						   PRIMARY KEY (tipologia_c, id_caso_c, ambiente_c)
						   )"""


error_table = """ CREATE TABLE IF NOT EXISTS Erros(
				   clima_e          VARCHAR(15) NOT NULL,
				   tipologia_e      VARCHAR(4) NOT NULL,
				   id_caso_e        VARCHAR(7) NOT NULL,
				   warning          TEXT,
				   severe           TEXT,
				   fatal            TEXT,
				   PRIMARY KEY (clima_e, tipologia_e, id_caso_e)
				   )"""

heating_table = """CREATE TABLE IF NOT EXISTS Aquecimento(
				   clima_a      VARCHAR(15) NOT NULL,
				   tipologia_a  VARCHAR(4) NOT NULL,
				   id_caso_a    VARCHAR(7) NOT NULL,
				   ambiente_a   VARCHAR(10) NOT NULL,
				   jan          FLOAT(8),
				   feb          FLOAT(8),
				   mar          FLOAT(8),
				   apr          FLOAT(8),
				   may          FLOAT(12),
				   jun          FLOAT(12),
				   jul          FLOAT(12),
				   aug          FLOAT(12),
				   sep          FLOAT(12),
				   oct          FLOAT(12),
				   nov          FLOAT(8),
				   dece         FLOAT(8),
				   anual        FLOAT(12),
				   PRIMARY KEY (clima_a, tipologia_a, id_caso_a, ambiente_a),
				   FOREIGN KEY (clima_a, tipologia_a, id_caso_a, ambiente_a) REFERENCES Caracteristica (clima_c, tipologia_c, id_caso_c, ambiente_c)
				   )"""

cooling_table = """CREATE TABLE IF NOT EXISTS Resfriamento(
				   clima_r      VARCHAR(15) NOT NULL,
				   tipologia_r  VARCHAR(4) NOT NULL,
				   id_caso_r    VARCHAR(7) NOT NULL,
				   ambiente_r   VARCHAR(10) NOT NULL,
				   jan          FLOAT(8),
				   feb          FLOAT(8),
				   mar          FLOAT(8),
				   apr          FLOAT(8),
				   may          FLOAT(12),
				   jun          FLOAT(12),
				   jul          FLOAT(12),
				   aug          FLOAT(12),
				   sep          FLOAT(12),
				   oct          FLOAT(12),
				   nov          FLOAT(8),
				   dece         FLOAT(8),
				   anual        FLOAT(12),
				   PRIMARY KEY (clima_r, tipologia_r, id_caso_r, ambiente_r),
				   FOREIGN KEY (clima_r, tipologia_r, id_caso_r, ambiente_r) REFERENCES Caracteristica (clima_c, tipologia_c, id_caso_c, ambiente_c)
				   )"""

time_table = """CREATE TABLE IF NOT EXISTS Tempo(
				   clima_t      VARCHAR(15) NOT NULL,
				   tipologia_t  VARCHAR(4) NOT NULL,
				   id_caso_t    VARCHAR(7) NOT NULL,
				   ambiente_t   VARCHAR(10) NOT NULL,
				   jan_1          REAL,
				   feb_1          REAL,
				   mar_1          REAL,
				   apr_1          REAL,
				   may_1          REAL,
				   jun_1          REAL,
				   jul_1          REAL,
				   aug_1          REAL,
				   sep_1          REAL,
				   oct_1          REAL,
				   nov_1          REAL,
				   dece_1         REAL,
				   anual_1        REAL,
				   jan_2          REAL,
				   feb_2          REAL,
				   mar_2          REAL,
				   apr_2          REAL,
				   may_2          REAL,
				   jun_2          REAL,
				   jul_2          REAL,
				   aug_2          REAL,
				   sep_2          REAL,
				   oct_2          REAL,
				   nov_2          REAL,
				   dece_2         REAL,
				   anual_2        REAL,
				   jan_3          REAL,
				   feb_3          REAL,
				   mar_3          REAL,
				   apr_3          REAL,
				   may_3          REAL,
				   jun_3          REAL,
				   jul_3          REAL,
				   aug_3          REAL,
				   sep_3          REAL,
				   oct_3          REAL,
				   nov_3          REAL,
				   dece_3         REAL,
				   anual_3        REAL,
				   Hdesconf     REAL,
				   Phoras       REAL,
				   PRIMARY KEY (clima_t, tipologia_t, id_caso_t, ambiente_t),
				   FOREIGN KEY (clima_t, tipologia_t, id_caso_t, ambiente_t) REFERENCES Caracteristica (clima_c, tipologia_c, id_caso_c, ambiente_c)
				   )"""

cursor.execute(charateristics_table)
cursor.execute(error_table)
cursor.execute(heating_table)
cursor.execute(cooling_table)
cursor.execute(time_table)

conn.close()
