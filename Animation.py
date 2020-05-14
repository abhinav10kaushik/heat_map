import collections
import matplotlib.animation as animation
import scipy.ndimage as ndimage
from Start import *


def animate_map(animation_record, map_image):

    if not animation_record:
        return

    x, y = convert_lat_long(*animation_record[4:6])

    if not 0 <= x <= 1 or not 0 <= y <= 1:
        return

    height, width = len(map_image), len(map_image[0])
    ax = plt.gca()
    ax.clear()
    ax.set_axis_off()
    ax.imshow(map_image)

    plt.plot(width * x, height * (1-y), 'o', markersize=10.0, color="red")
    plt.text(
        width * x, height * (1-y), "{}\n  Spd: {}m/s".format(animation_record[7], animation_record[6]))


# Get the data set
data_set = read_data_set("Cyclones.csv")

# Parse it into the required format
for index, record in enumerate(data_set):
    data_set[index] = parse_record(record)

# Separate the data out by storm id
storms = collections.defaultdict(list)
for record in data_set:
    storms[record["id"]].append(record)

# Generate the storm track data
storm_tracks = dict()
for storm, record_list in storms.items():
    storm_tracks[storm] = animation_data(record_list)

map_image = ndimage.imread("Australia_Map.jpg")

animation_track = []

# Filter the data to only include records on the map
for storm in storm_tracks.values():
    for time_stamp in storm:
        x, y = convert_lat_long(*time_stamp[4:6])

        if not 0 <= x <= 1 or not 0 <= y <= 1:
            continue
        animation_track.append(time_stamp)

# show map
fig = plt.figure()
plt.ioff()

ax = plt.axes([0, 0, 1, 1])
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(map_image)


# Produce the animation
display = animation.FuncAnimation(fig, animate_map, interval=100, repeat=False,
                                  fargs=(map_image,),
                                  frames=animation_track)
plt.show()
