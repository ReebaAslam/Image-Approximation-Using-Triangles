import numpy as np

class Evolve:
    '''Base class for evolution'''
    def __init__(self,PopSize):
        self.PopSize=PopSize
        self.Population=self.GenerateRandom()
        self.TotalFitness=0
        self.Sort()
        self.Total()
        self.AvgFitness=self.TotalFitness/self.PopSize
        self.BestChromo=self.Population[0]
        self.BestFitness=self.BestChromo.Fitness
        self.GenerationNo=0

    def GenerateRandom(self):
        pass

    def SetAttributes(self):
        self.Sort()
        self.Total()
        self.AvgFitness=self.TotalFitness/self.PopSize
        self.BestChromo=self.Population[0]
        self.BestFitness=self.BestChromo.Fitness
    
    def Total(self):
        sum=0
        for each in self.Population:
            sum+=each.Fitness
        self.TotalFitness=sum
    
    def Sort(self):
        self.Population = sorted(self.Population, key=lambda x: x.Fitness)
        
    def crossover(self,SType):
        pass
    def mutate(self):
        pass
    
    def select(self,SType='FPS'):
        #survivor selection
        #SType -> Selection Type
        survivors=[]
        p=self.PopSize
        if SType=='FPS':
            survivors=self.FPS(p)
        elif SType=='RBS':
            survivors=self.RBS(p)
        elif SType=='BTS':
            survivors=self.BTS(p)
        elif SType=='Random':
            survivors=self.RandomS(p)
        elif SType=='Truncate':
            survivors=self.TruncateS(p)
        else:
            raise ValueError("Wrong Selection Type")
        self.GenerationNo+=1
        self.Population=survivors
        
    def FPS(self,n):
        #Fitness Proportional Selection
        self.SetAttributes()
        pop=self.Population
        probs=[]
        for each in pop:
            p=each.Fitness/self.TotalFitness
            probs.append(1-p)
        selected=[]
        for i in range(n):
            rand=np.random.uniform(probs[-1],probs[0]+0.08)
            index=BinarySearch(probs,rand,0,len(probs)-1)
            selected.append(self.Population[index])
        return selected
            
            
    def RBS(self,n):
        #Rank Based Selection
        self.SetAttributes()
        pop=self.Population
        selected=[]
        ranks=[]
        r=0
        last=pop[0]
        for each in pop:
            if each.Fitness!=last.Fitness:
                r+=1
            ranks.append(r)
            last=each
        total=len(pop)*(len(pop)+1)/2
        probs=[]
        for i in ranks:
            p=float(len(pop)-i)/float(total)
            probs.append(p)
        for i in range(n):
            rand=np.random.rand()
            index=BinarySearch(probs,rand,0,len(probs)-1)
            selected.append(self.Population[index])
        return selected
    
    def BTS(self,n):
        #Binary Tournament Selection
        pop=self.Population[:]
        selected=[]
        for i in range(n):
            first=pop[np.random.randint(0,len(pop))]
            sec=pop[np.random.randint(0,len(pop))]
            if sec.Fitness<first.Fitness:
                selected.append(sec)
            else:
                selected.append(first)
        return selected
        
    def RandomS(self,n):
        #Random Selection
        pop=self.Population
        selected=[]
        for i in range(n):
            selected.append(np.random.choice(pop))
        return selected
    
    def TruncateS(self,n):
        #Truncation Selection
        self.SetAttributes()
        selected=self.Population[0:n]
        np.random.shuffle(selected)
        return selected

    

    
def BinarySearch(lst,k,ind1,ind2):      #helper function
    length=ind2-ind1+1
    if length==1:
        return ind1
    elif length<1:
        raise ValueError("Input correct list")
    elif k>lst[0]:
        return 0
    elif k<lst[-1]:
        return 1
    else:
        mid=length//2 + ind1
        more=mid-1
        less=mid+1
        if ind2==mid:
            more=mid
        if ind1==mid or less>ind2:
            less=mid
        if less==more:
            return less
        if k>=lst[mid]:
            if k<lst[more]:
                return mid
            else:
                return BinarySearch(lst,k,ind1,more)
        else:
            if k>=lst[less]:
                return less
            else:
                return BinarySearch(lst,k,less,ind2)  
