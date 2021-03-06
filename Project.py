### Hans Rosling's animated plot
### 22th of April 2022


# import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import imageio

# get data
fert = pd.read_csv("data/gapminder_total_fertility.csv", index_col=0)
pop = pd.read_excel("data/gapminder_population.xlsx", index_col=0, nrows=260)
life = pd.read_excel("data/gapminder_lifeexpectancy.xlsx", index_col=0)


# convert columns from string to integer
fert.columns = fert.columns.astype(int)

# check row index of tables and change its name
fert.index.name = "country"

# Converting fert table to long format
fert = fert.reset_index()
fert = fert.melt(id_vars="country", var_name="year", value_name="fertility_rate")

# Converting life table to long format
life.index.name = "country"
life = life.reset_index()
life = life.melt(id_vars="country", var_name="year", value_name="life_expectancy")

# Converting pop table to long format
pop.index.name = "country"
pop = pop.reset_index()
pop = pop.melt(id_vars="country", var_name="year", value_name="population")

# Merging the DataFrames
df = fert.merge(pop)
df = df.merge(life)

# Plot life expectancy to fertility rate in the year 2000
df_subset = df.loc[df["year"] == 2000]
sns.scatterplot(x="life_expectancy", y="fertility_rate", data=df_subset, alpha=0.6)
plt.close()


# Create multiple Plots of life expectancy, fertility rate and population
for date in pd.unique(df["year"]):
	if date < 1960:
		pass
	else:
		plt.axis((10,90,0,10))
		df_subset_x = df.loc[df["year"] == date]
		popsize = df_subset_x["population"]*1000
		sns.scatterplot(x="life_expectancy", y="fertility_rate", size="population", sizes=(10, 200), data=df_subset_x, alpha=0.6, legend=False)
		plt.savefig(fname=("lifeexp_images/lifeexp_"+str(date)), format="png")
		plt.close()

# Create gif
images = []

for i in range(1960,2015):
	filename = "lifeexp_images/lifeexp_{}".format(i)
	images.append(imageio.imread(filename))

imageio.mimsave("output.gif", images, fps=20)