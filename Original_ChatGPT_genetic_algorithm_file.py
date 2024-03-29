@classmethod
    #Main function that implements the genetic algorithm. Takes several parameters.
    #
    def genetic_algorithm(cls, objective, n_bits, n_iter, n_pop, r_cross, r_mut, r_ins, r_del):
        # initial population of random bitstring
        pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
        # keep track of best solution
        best, best_eval = 0, objective(pop[0])
        # enumerate generations
        for gen in range(n_iter):
            # evaluate the fitness of all candidates in the population
            scores = [objective(c) for c in pop]
            # check for new best solution
            for i in range(n_pop):
                if scores[i] < best_eval:
                    best, best_eval = pop[i], scores[i]
                    print(">%d, new best f(%s) = %.3f" % (gen, pop[i], scores[i]))
            # select parents
            selected = [cls._selection(pop, scores) for _ in range(n_pop)]
            # create the next generation
            children = list()
            for i in range(0, n_pop, 2):
                # get selected parents in pairs
                p1, p2 = selected[i], selected[i + 1]
                # crossover and mutation
                for c in cls._crossover(p1, p2, r_cross, r_ins, r_del):
                    # mutation
                    cls._mutation(c, r_mut, r_ins)
                    # store for next generation
                    children.append(c)
            # replace population
            pop = children
        return [best, best_eval]

    @classmethod
    def _selection(cls, pop, scores, k=3):
        # first random selection
        selection_x = randint(len(pop))
        for x in randint(0, len(pop), k - 1):
            # check if better (e.g. perform a tournament)
            if scores[x] < scores[selection_x]:
                selection_x = x
        return pop[selection_x]
    
    @classmethod
    def _insertion(cls, bitstring, r_ins):
        """
        Perform insertion mutation on the given bitstring.

        Parameters:
        - bitstring (list): The bitstring to perform insertion mutation on.
        - r_ins (float): The insertion rate, determining the likelihood of insertion.
        """
        for i in range(len(bitstring)):
            # check for insertion mutation
            if rand() < r_ins:
                # insert a random bit at a random position
                bitstring.insert(randrange(len(bitstring)), randint(0, 2))

    
    @classmethod
    def _deletion(cls, bitstring):
            """
            Perform deletion mutation on the given bitstring.

            Parameters:
            - bitstring (list): The bitstring to perform deletion mutation on.
            """
            # delete a random bit
            del bitstring[randrange(len(bitstring))]
        
        

    @classmethod
    def _crossover(cls, p1, p2, r_cross, r_ins, r_del, max_children_per_parent = 20):
        # children are copies of parents by default
        c1, c2 = p1.copy(), p2.copy()
    
        # Track the number of children generated for each parent
        num_children_c1, num_children_c2 = 0, 0
    
        # check for recombination
        if random() < r_cross:
            # perform even crossover
            crossover_point_even = randrange(len(p1))
            c1_even = p1[:crossover_point_even] + p2[crossover_point_even:]
            c2_even = p2[:crossover_point_even] + p1[crossover_point_even:]

            # perform uneven crossover
            pt = randint(1, len(p1) - 2)
            c1_uneven = p1[:pt] + p2[pt:]
            c2_uneven = p2[:pt] + p1[pt:]

            # decide whether to perform insertion for even crossover
            if random() < r_ins:
                cls._insertion(c1_even, r_ins)
                num_children_c1 += 1

            # decide whether to perform insertion for uneven crossover
            if random() < r_ins:
                cls._insertion(c2_uneven, r_ins)
                num_children_c2 += 1

            # decide whether to perform deletion for even crossover
            if random() < r_del and len(c1_even) > 1:
                cls._deletion(c1_even)
                num_children_c1 -= 1

            # decide whether to perform deletion for uneven crossover
            if random() < r_del and len(c2_uneven) > 1:
                cls._deletion(c2_uneven)
                num_children_c2 -= 1

            # Check if the number of children exceeds the limit
            if num_children_c1 >= max_children_per_parent:
                c1_even, c2_even = [], []  # Empty lists to indicate no more children
            if num_children_c2 >= max_children_per_parent:
                c1_uneven, c2_uneven = [], []  # Empty lists to indicate no more children

            # return both even and uneven crossover children as flat lists
            return [c1_even, c2_even, c1_uneven, c2_uneven]

        # if no recombination, return the original parents as flat lists
        return [c1, c2]
    
    @classmethod
    def _mutation(cls, bitstring, r_mut, r_ins):
        """
        Perform mutation on the given bitstring.
        Parameters:
        - bitstring (list): The bitstring to perform mutation on.
        -  r_mut (float): The mutation rate, determining the likelihood of mutation.
        - r_ins (float): The insertion rate, determining the likelihood of insertion.

        Returns:
        - list: The mutated bitstring.
        """
        for i in range(len(bitstring)):
            # check for mutation
            if rand() < r_mut:
                # flip the bit
                bitstring[i] = 1 - int(bitstring[i])

