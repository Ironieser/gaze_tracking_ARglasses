import pandas as pd
import numpy as np


df = pd.DataFrame(np.zeros(24).reshape((6,4)),columns=['world_x','world_y','eye_x','eye_y'])
print(df)
df.iloc[5,2]=66
print(df)