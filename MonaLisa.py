from Evo import Evolve
from PIL import Image, ImageDraw, ImageChops
import numpy as np
from functools import reduce
import operator
import time

#Parameters
POP_SIZE=5
NO_OF_KIDS=4
GEN_COUNT=50000
MUTATION_RATE=0.1

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#no. of polygons
COUNT = 500
#target image
TARGET = Image.open('test.png').convert('RGB')
SIZE=TARGET.size
i1 = np.array(TARGET, np.int16)
a=SIZE[0]*SIZE[1]/2000

class Gene:     #stores attributes of a polygon
    def __init__(self):
        self.pos1 = (np.random.randint(0, SIZE[0]), np.random.randint(0, SIZE[1]))
        self.pos2 = (np.random.randint(self.pos1[0]-a, self.pos1[0]+a), np.random.randint(self.pos1[1]-a, self.pos1[1]+a))
        self.pos3 = (np.random.randint(self.pos1[0]-(a+5), self.pos1[0]+(a+5)), np.random.randint(self.pos1[1]-(a+5), self.pos1[1]+(a+5)))
        self.RGBA = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        
class MLChromosome:     #comprises of multiple polygons
    def __init__(self,n,random=True):   
        self.PolCount=n
        self.Genes=[]
        self.GenerateGenes(random)
        self.Image=self.GenerateImage(self.Genes)
        self.Fitness=self.CalculateFitness(im=self.Image)

    def GenerateGenes(self,random=True):
        #random= True-> random polygon
        #random= False-> a good chromosome(sol) is generated
        if random==False:
            g=[]
            img=self.GenerateImage(g)
            for i in range(self.PolCount):
                sample=[]
                fit=(348928340283048,0)
                for j in range(50):
                    sample.append(Gene())
                    img=self.GenerateImage(g+[sample[j]])
                    f=self.CalculateFitness(img)
                    if f<fit[0]:
                        fit=(f,j)
                g.append(sample[fit[1]])
            self.Genes=g
        else:
            for i in range(self.PolCount):
                self.Genes.append(Gene())        

    def GenerateImage(self,genes):
        im = Image.new('RGB', SIZE, BLACK)
        draw = ImageDraw.Draw(im, 'RGBA')
        for poly in genes:
            draw.polygon([poly.pos1, poly.pos2, poly.pos3], fill=poly.RGBA, outline=poly.RGBA)
        del draw
        return im

    def CalculateFitness(self,im):
        i2 = np.array(im, np.int16)
        dif = np.sum(np.abs(i1 - i2))
        pos = (dif / 255.0 * 100) / i1.size
        h = ImageChops.difference(TARGET, im).histogram()
        pix = np.sqrt(reduce(operator.add,
                             list(map(lambda h, i: h * (i ** 2),
                                      h, list(range(256)) * 3))) /
                      (float(SIZE[0]) * SIZE[1]))
        return pix + pos

    def SetGenes(self,g):
        self.Genes=g
        self.Image=self.GenerateImage(self.Genes)
        self.Fitness=self.CalculateFitness(im=self.Image)


class MLEvolve(Evolve):     #child class of Evolve for Mona Lisa Approximation
    def __init__(self,PopSize=POP_SIZE):
        Evolve.__init__(self,PopSize)

    def GenerateRandom(self, random=True):
        pop=[]
        for i in range(self.PopSize):
            print("population generating...")
            if i%2==0 and random==False:
                pop.append(MLChromosome(COUNT,False))
            else:
                pop.append(MLChromosome(COUNT))
        return pop

    def crossover(self,SType='FPS'):    
        parents=[]
        offsprings=[]
        if SType=='FPS':
            parents=self.FPS(NO_OF_KIDS)
        elif SType=='RBS':
            parents=self.RBS(NO_OF_KIDS)
        elif SType=='BTS':
            parents=self.BTS(NO_OF_KIDS)
        elif SType=='Random':
            parents=self.RandomS(NO_OF_KIDS)
        elif SType=='Truncate':
            parents=self.TruncateS(NO_OF_KIDS)
        else:
            return ValueError('Wrong Selection Name!')
        i=0
        j=1
        while j<NO_OF_KIDS:
            r1=np.random.randint(0,self.PopSize-1)
            r2=np.random.randint(0,self.PopSize-1)
            father=parents[i].Genes
            mother=parents[j].Genes
            son=mother[:r1]+father[r1:r2]+mother[r2:]
            daughter=father[:r1]+mother[r1:r2]+father[r2:]
            offsprings.append(daughter)
            offsprings.append(son)
            i+=2
            j+=2
        return offsprings

    def mutate(self,children):
        for kid in children:
            for i in range(len(kid)):
                if np.random.rand()<=MUTATION_RATE:
                    gene = Gene()
                    kid[i] = gene
            chromo=MLChromosome(COUNT)
            chromo.SetGenes(kid)
            self.Population.append(chromo)
            
    def run(self,SType1='FPS',SType2='FPS'):
        global MUTATION_RATE
        print("Generation #",self.GenerationNo, " Best: ", self.BestFitness, " Average: ", self.AvgFitness) 
        self.BestChromo.Image.save("gen#"+str(self.GenerationNo)+".png")
        start=time.time()
        while self.GenerationNo<GEN_COUNT:
            offsprings=self.crossover(SType1)
            self.mutate(offsprings)
            self.select(SType2)
            self.SetAttributes()
            if self.GenerationNo%50==0:
                print("Generation #",self.GenerationNo, " Best: ", self.BestFitness, " Average: ", self.AvgFitness)
            if self.GenerationNo in [0,500] or self.GenerationNo%1000==0:
                self.BestChromo.Image.save("gen#"+str(self.GenerationNo)+".png")
                end=time.time()
                print(end-start)
            if self.GenerationNo%2000==0:   #simulated annealing added
                MUTATION_RATE*=0.8
            

ml=MLEvolve(POP_SIZE)
#can only use these key words to run the function [FPS, RBS, Random, BTS, Truncate]
ml.run('Random','RBS')
        
        
