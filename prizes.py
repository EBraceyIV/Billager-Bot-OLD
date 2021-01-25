import discord

# Rarity colors:
rarities = ["Common", "Peculiar", "Perplexing", "Mystifying", "Fantasmaglorical"]
values = ["1 ᘋ - 1000 ᘋ", "1001 ᘋ - 5000 ᘋ", "5001 ᘋ - 10000 ᘋ", "10001 ᘋ - 100000 ᘋ", "100001 ᘋ +"]
common = 0x150549
peculiar = 0xff22df
perplexing = 0xf0ff00
mystifying = 0xff4d00
fantasmaglorical = 0x00ecff

PRIZES = {"seagull": [discord.Embed(title="Seagull",
                                    description="Flying coast rat.",
                                    color=common),
                      "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Larus_occidentalis_%28Western_Gull%29%2C_Point_Lobos%2C_CA%2C_US_-_May_2013.jpg/1200px-Larus_occidentalis_%28Western_Gull%29%2C_Point_Lobos%2C_CA%2C_US_-_May_2013.jpg",
                      "50",
                      "Common"],

          "wills shoes": [discord.Embed(title="Will's Shoes",
                                         description="They're worth so little because he owns so many.",
                                         color=common),
                           "http://www.fantastischekinderdisco.be/clown_shoes.png",
                           "2",
                           "Common"],

          "coconut": [discord.Embed(title="Coconut",
                                    description="It's a coconut. The coconut is the proud owner of both hair and milk, "
                                                "which qualifies it as a mammal. Deadly when falling from its tropical "
                                                "treetop abode, the coconut also demonstrates the killer instinct "
                                                "necessary for survival in the animal kingdom. This may be your prize "
                                                "but make no mistake, you do not own the coconut. "
                                                "Nobody should dare to try.",
                                    color=peculiar),
                      "https://d3cizcpymoenau.cloudfront.net/images/28285/SIL_CoconutProducts_Cracked_05.png",
                      "200",
                      "Peculiar"],

          "elliotts gamer chair": [discord.Embed(title="Elliott's Gamer Chair",
                                                  description="A throne for a true king. This vessel will support you "
                                                              "through gaming sessions upwards of 17 hours at a time. "
                                                              "That familiar comforting scent is sure to put you at "
                                                              "ease and allow your mind to focus solely on the task at "
                                                              "hand: bideo gaem.",
                                                  color=peculiar),
                                    "https://lh3.googleusercontent.com/-VgWN4JntMXE/VWUN1dANdkI/AAAAAAAAHpc/1gZrYKR2Sv4/s640/blogger-image-271844959.jpg",
                                    "500",
                                    "Peculiar"],

          "lava lamp": [discord.Embed(title="Lava Lamp",
                                      description="Hot goo in a funky tube. No ticket prize shelf or psychedelic "
                                                  "bachelor pad is complete without one. Enter a magical trance and "
                                                  "watch those enchanting blobs bounce about. Be warned, however. Do "
                                                  "not attempt to include one of these in your carry-on baggage when "
                                                  "using commercial air travel. An RPG-shaped object full of liquid "
                                                  "that sets off the x-ray machine is something best left to your "
                                                  "checked bag and not to be prodded by a TSA agent in front of you.",
                                      color=perplexing),
                        "https://www.lavalamp.com/wp-content/uploads/2017/07/2700.png",
                        "5000",
                        "Perplexing"],

          "mcdonalds chicken caesar salad": [discord.Embed(title="McDonald's Chicken Caesar Salad",
                                                            description="Infinite Sandwich",
                                                            color=perplexing),
                                              "http://theloadedslice.net/image/cache/products/salads/chicken-caesar-salad-800x800.png",
                                              "3999",
                                              "Perplexing"],

          # TODO: Add "bonus stats" like, +4 Mcdonald's craving
          "juniels beard clippings": [discord.Embed(title="Juniel's Beard Clippings",
                                                     description="He can grow this easily, the blueberries not so "
                                                                 "much. Those lucky enough to brustle this beard are "
                                                                 "considered his truest friends.",
                                                     color=perplexing),
                                       "https://scottburns.files.wordpress.com/2011/12/img_0424.jpg",
                                       "7220",
                                       "Perplexing"],

          "chuys gift card": [discord.Embed(title="Chuy's Gift Card",
                                             description="A blessed meal at no cost to you. Fajitas, burritos, "
                                                         "flautas, and of course a bowl of hot queso. All of this and "
                                                         "more could be yours. Dine at the Chihuahua Bar and feel "
                                                         "those fantastic Mexican calories engorge your very soul.",
                                             color=mystifying),
                               "https://nypizzahollywood.com/wp-content/uploads/2018/11/chuys-gift-card-1.png",
                               "60000",
                               "Mystifying"],

          "dans car": [discord.Embed(title="Dan's Car",
                                      description="Like a father and his son, Dan built this mean machine with his own "
                                                  "two hands in his garage. This spicy vroomer has unlimited vehicular "
                                                  "potential. A whole engine, all the tires, seats, a full tank of "
                                                  "headlight fluid, and legal dispensation to drive an extra 3 miles "
                                                  "per hour in any school zone. The open road beckons, will you answer "
                                                  "the call?",
                                      color=fantasmaglorical),
                        "https://vignette3.wikia.nocookie.net/deathbattlefanon/images/a/a8/DC_Comics_-_The_Batmobile_1960s_era.png/revision/latest?cb=20160527111804",
                        "200000",
                        "Fantasmaglorical"],

          "pee wees bike": [discord.Embed(title="Pee Wee's Bike",
                                           description="Found in the basement of the Alamo.",
                                           color=fantasmaglorical),
                             "https://jasonvorhees.files.wordpress.com/2012/05/pee-wee-bike.jpg",
                             "500000",
                             "Fantasmaglorical"]
          }


def prizes():
    return PRIZES
