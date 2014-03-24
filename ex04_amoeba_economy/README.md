##amoeba life in more or less zen situations

Some virtues of object-oriented programming should become pretty obvious when tinkering with these examples of simulations of interacting balls/marbles/amoebae/particles.

####more goals
Find stable regimes of evolving populations.
- This may help understand some population-related aspects of the theory of evolution.
- It may also help understand economics: think of the mushrooming balls as representing companies. Why does Europe have no Silicon Valley? Why did the US become deindustrialised? There is a balance to be found between game rules supporting the mushrooming of new entities and on the other hand the factors increasing the probability of longer-term existence. Well, macroeconomics on the international level is a bit more complicated, e.g. there are populations of companies with different internal rules (laws at home) competing globally, but why not try something like that also with the amoebae?

#### challenges
- Take these examples as inspiration and invent new species and new rules deciding what happens upon amoebae encounters.
- After some inspiring tinkering, decide on what you want to simulate, then code it up, and finally run experiments and find a setup leading to a stable regime.
- Implement simplified poker games upon encounter, where the betting strategies are subject to evolution.


The last challenge idea goes back to an article I have read of 1967 from three founding fathers of evolutionary computation: "Simulation of biological evolution and machine learning: I. Selection of self-reproducing numeric patterns by data processing machines, effects of hereditary control, mutation type and crossing" by Jon Reed, Robert Toombs, and Nils Aall Barricelli, Journal of Theoretical Biology, volume 17 (1967), issue 3, pp. 319-342. Here the short description of their simulation:

Individuals have to compete in a simplified game of poker and have to develop optimal betting strategies in competition with each other. Always two individuals compete in 20 rounds of the simple game and the goal is to win more often than the opponent. Individuals are given, by random, one symbol either representing a good or a bad hand of cards at the beginning of each round. The DNA of an individual determines what it does upon recieving the symbol. On good or bad hand it can either bet on high, low, or pass. The costs of the bets ``pass'', ``low'', and ``high'' are 2, 3, and 7 pennies, respectively. Because for each of the two situations ``low hand'' and ``high hand'' there are three betting probabilities which must add to 1, there are in total four betting strategy parameters to tune. After both individuals have made their bets, always the one who has placed the higher bet wins, no matter what the real hands are, and only if the two bets are the same, then the actual hands themselves count and are able to decide the winner or a tie. The game is simple enough that game theory can determine the optimal betting probabilities. The coevolutionary result can then be compared against this benchmark.
