from qiskit import *
from sys import*

print("Choose your board size: from 4-10")
n = int(input())

turns = 1
#p1 = []
exit = []
p = []
game = True
bits = "0"*n
arnab = [[" " for y in range(n)]
            for x in range(n)]
classical = []
control_list = []
target_list = []
entry = []
w = 0
b = 0

def board(lis):
    #global n
    g = len(lis)
    for i in range(g):

        for j in range(g-1):
            print(lis[i][j],end="")
            print(" ---",end=" ")
        print(lis[i][g-1])
        if i == g-1:
            break
        else:
            print("|     "*(g-1),end="")
            print("|")

circuit = QuantumCircuit(n**2,n**2)

def setup():
    for i in range(n**2):
        circuit.h(i)
    print("Legal Moves:")
    print("Classical Move(c): Collapses Box to 'W(White)' or 'B(Black)' with equal probability");
    print("Quantum Move(q): Entangles target box and control box. Reverses target box if control box collapses in your favour");
    print(" ")
    print("Rules:")
    print("1) Initially all boxes are in Quantum State/superposition of 'W' and 'B'")
    print("2) Only Classical move can collapse a quantum state to a classical state")
    print("3) A  classical  move  can  only  be  applied  to  a  box  that  is in Quantum State i.e. a classical  move cannot be apllied to the same box twice")
    print("4) The Quantum Move’s target box should be in a Classical State, and the control box should be in a Quantum State")
    print("5) If a player chooses to pass and the next player also chooses to pass, the game is over.")
    print("   Otherwise game continues...")
    print("6) Other rules are same as the Classical Go Game.")
    print(" ")

def turn():
    global turns
    global exit
    if turns%2 == 1:
        print("Black player's turn")
    elif turns%2 == 0:
        print("White player's turn")
    print("Enter C for Classical move, Q for Quantum move or P to pass")
    m = input().lower()
    if m == "c":
        print("Enter position(1 -",n**2,")")
        p.append(int(input())-1)
        cmove(int(p[len(p)-1])+1)
    elif m == "q":
        control = int(input("Enter Control Position(1-25): "))
        target = int(input("Enter Target Position(1-25): "))
        qmove(control-1,target-1)
    elif m == "p":
        print("Does the other player also want to pass?(Y/N)")
        res = input().lower()
        if turns%2 == 1:
            if res == "y":
                game = False
                print("Game over")
            else:
                turns+=1
                b+=1
                turn()
        else:
            if res == "y":
                print("Does the other player also want to pass?(Y/N)")
                res1 = input().lower()
                if res1 == "y":
                    game = False
                    print("Game over")
                else:
                    turns+=1
                    w+=1
                    turn()
            else:
                turns+=1
                turn()
                w+=1
    else:
        print(" ")
        print("Illegal move")
        print(":)")
        turn()

def cmove(pos):
    global turns
    global bits
    global  game
    #global entry
    global p
    #global p1
    circuit.measure(pos-1,n**2-pos)
    simulator=Aer.get_backend('qasm_simulator')
    job = execute(circuit,backend=simulator,shots=1)
    result = job.result()
    pq=result.get_counts(circuit)
    #print(pq)
    p1 = list(pq)
    bits=p1[0]
    #print(ps[pos-1])
    #print(ps)

    if pos not in classical:
        if(bits[pos-1]=='1'):
            x=1
            circuit.reset(pos-1)
            circuit.x(pos-1)
            circuit.measure(pos-1,n**2-pos)
        else:
            x=0
            circuit.reset(pos-1)
            circuit.measure(pos-1,n**2-pos)
        if pos-1 in control_list:
            i=control_list.index(pos-1)
            if entry[i]=="B":
                circuit.cx(pos-1,target_list[i])
                circuit.measure(target_list[i],n**2-1-target_list[i])

            else:
                circuit.x(pos-1)
                circuit.cx(pos-1,target_list[i])
                circuit.x(pos-1)
                circuit.measure(target_list[i],n**2-1-target_list[i])

    else:
        print(" ")
        print("Illegal move")
        turns = turns - 1
    classical.append(pos)
    turns+=1
    mark(bits)
    ps=p1[0]
    if game==True:
        turn()

def qmove(control,target):
    global turns
    global target_list
    global control_list
    global classical
    if target+1 in classical and control+1 not  in classical:
        target_list.append(target)
        control_list.append(control)

        if turns%2==0:
            entry.append("W")
        else:
            entry.append("B")
        print(control+1,'-',target+1,' ',"entangled")

    else :
        print(" ")
        print("Illegal move")
        turns = turns - 1
    turns = turns + 1
    turn()
def remove(list):
    global w
    global b
    for i in range(1,len(list)-1):
        for j in range(1,len(list)-1):
            if list[i][j]=="W":
                if list[i-1][j]=="B" and list[i+1][j]=="B" and list[i][j-1]=="B" and list[i][j+1]=="B":
                    list[i][j] = " "
                    w+=1
                    #turn()
            elif list[i][j]=="B":
                if list[i-1][j]=="W" and list[i+1][j]=="W" and list[i][j-1]=="W" and list[i][j+1]=="W":
                    list[i][j] = " "
                    b+=1
                    #turn()
    for i in range(1,len(list)-1):
        if list[i][0]=="W":
            if list[i-1][0]=="B" and list[i+1][0]=="B" and list[i][1]=="B":
                list[i][0] = " "
                b+=1
                #turn()
        elif list[i][0]=="B":
            if list[i-1][0]=="W" and list[i+1][0]=="W" and list[i][1]=="W":
                list[i][0] = " "
                w+=1
                #turn()
        elif list[0][i]=="W":
            if list[0][i-1]=="B" and list[0][i+1]=="B" and list[1][i]=="B":
                list[0][i] = " "
                b+=1
                #turn()
        elif list[0][i]=="B":
            if list[0][i-1]=="W" and list[0][i+1]=="W" and list[1][i]=="W":
                list[0][i] = " "
                w+=1
                #turn()
    if list[0][0]=="W":
        if list[1][0]=="B" and list[0][1]=="B":
            list[0][0]=" "
            b+=1
            #turn()
    elif list[0][0]=="B":
        if list[1][0]=="W" and list[0][1]=="W":
            list[0][0] = " "
            w+=1
            #turn()
    if list[0][len(list)-1]=="W":
        if list[1][len(list)-1]=="B" and list[0][len(list)-2]=="B":
            list[0][len(list)-1] = " "
            b+=1
            #turn()
    elif list[0][len(list)-1]=="B":
        if list[1][len(list)-1]=="W" and list[0][len(list)-2]=="W":
            list[0][len(list)-1] = " "
            w+=1
            #turn()
    if list[len(list)-1][len(list)-1]=="W":
        if list[len(list)-1][len(list)-2]=="B" and list[len(list)-2][len(list)-1]=="B":
            list[len(list)-1][len(list)-1] = " "
            b+=1
            #turn()
    elif list[len(list)-1][len(list)-1]=="B":
        if list[len(list)-1][len(list)-2]=="W" and list[len(list)-2][len(list)-1]=="W":
            list[len(list)-1][len(list)-1] = " "
            w+=1
            #turn()
    if list[len(list)-1][0]=="W":
        if list[len(list)-2][0]=="B" and list[len(list)-1][1]=="B":
            list[len(list)-1][0] = " "
            b+=1
            #turn()
            #turn()
    elif list[len(list)-1][0]=="B":
        if list[len(list)-2][0]=="W" and list[len(list)-1][1]=="W":
            list[len(list)-1][0] = " "
            w+=1
    return list
    turn()
    #board(remove(arnab))

def mark(bits):
    global p
    global game
    simulator=Aer.get_backend('qasm_simulator')
    result=execute(circuit,backend=simulator,shots=1).result()
    pq=result.get_counts(circuit).keys()
    pl=list(pq)
    bits = pl[0]
    for i in range(len(p)):
        r=int(p[i]/n)
        c=int(p[i]%n)
        if bits[p[i]]=='1':
            arnab[r][c]='B'
        else:
            arnab[r][c]='W'
    board(remove(arnab))
    print(w,b)

setup()
turn()
