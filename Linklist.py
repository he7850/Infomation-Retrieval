import Gamma

class Node(object):
    def __init__(self,val,p=0):
        self.docno = val[0]
        self.tf = val[1]
        self.next = p

class LinkList(object):
    def __init__(self):
        self.head = 0

    def __getitem__(self, key):

        if self.is_empty():
            print('linklist is empty.')
            return

        elif key <0  or key > self.getlength():
            print('the given key is error')
            return

        else:
            return self.getitem(key)



    def __setitem__(self, key, value):

        if self.is_empty():
            print('linklist is empty.')
            return

        elif key <0  or key > self.getlength():
            print('the given key is error')
            return

        else:
            self.delete(key)
            return self.insert(key)

    def initlist(self,data):

        self.head = Node(data[0])

        p = self.head

        for i in data[1:]:
            node = Node(i)
            p.next = node
            p = p.next

    def getlength(self):

        p =  self.head
        length = 0
        while p!=0:
            length+=1
            p = p.next

        return length

    def is_empty(self):

        if self.getlength() ==0:
            return True
        else:
            return False

    def clear(self):

        self.head = 0


    def append(self,item):
        pre = self.head
        curr = self.head
        temp = item[0]
        if self.head ==0:
            self.head = Node(item)
            return
        else:
            val = curr.docno
            curr = curr.next
            while curr!= 0:
                val += Gamma.__gammaUncompress__(curr.docno)
                pre = curr
                curr = curr.next
            #val += Gamma.__gammaUncompress__(curr.docno)
            item[0] = Gamma.__gamma__(temp-val)
            pre.next = Node(item)


    def getitem(self,index,double=False):

        if self.is_empty():
            print('Linklist is empty.')
            return
        j = 0
        p = self.head

        while p.next!=0 and j <index:
            p = p.next
            j+=1

        if j ==index:
            if not double:
                return p.docno
            elif double:
                return p.docno,p.tf

        else:

            print ('target is not exist!')

    def insert(self,index,item):

        if self.is_empty() or index<0 or index >self.getlength():
            print ('Linklist is empty.')
            return

        if index ==0:
            q = Node(item,self.head)

            self.head = q

        p = self.head
        post  = self.head
        j = 0
        while p.next!=0 and j<index:
            post = p
            p = p.next
            j += 1

        if index ==j:
            q = Node(item,p)
            post.next = q
            q.next = p


    def delete(self,index):

        if self.is_empty() or index<0 or index >self.getlength():
            print('Linklist is empty. or Index Error')
            return

        if index == 0:
            self.head = self.head.next

#        if index ==0:
#           q = Node(item,self.head)

#            self.head = q

        p = self.head
        post  = self.head
        j = 0
        while p.next!=0 and j<index:
            post = p
            p = p.next
            j+=1

        if index ==j:
            post.next = p.next

    def index(self,value):

        if self.is_empty():
            print('Linklist is empty.')
            return

        p = self.head
        i = 0
        while p.next!=0 and not p.docno ==value:
            p = p.next
            i+=1

        if p.docno == value:
            return i
        else:
            return -1

    def increase(self,value):
        if self.is_empty():
            #print('Linklist is empty.')
            return False
        p = self.head
        docno_val=p.docno
        while p.next!=0 and not docno_val == value:
            p = p.next
            docno_val += Gamma.__gammaUncompress__(p.docno)
        if docno_val == value:
            p.tf+=1
            return True
        else:
            return False
    def output(self):
        p = self.head
        if p == 0:
            print('empty')
        s= ''
        count = p.docno
        s += str(count)
        s += ','
        s += str(p.tf)
        s += '|'
        p = p.next
        while p!=0:
            #print(count)
            count += Gamma.__gammaUncompress__(p.docno)
            s += str(count)
            #print('add : ',)
            s += ','
            s += str(p.tf)
            s += '|'
            p = p.next
        return s
'''
list_test = LinkList()
data = [['a',1],['b',2],['c',1]]
list_test.initlist(data)
print(list_test.getitem(2,True))
list_test.increase('c')
print(list_test.getitem(2,True))
list_test.append(['d',2])
print(list_test.output())
'''