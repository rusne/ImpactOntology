import owlready2 as owl

owl.onto_path.append('/Users/rusnesileryte/Google Drive/PhD/Ontology')
onto = owl.get_ontology('exampleBooks.owl')
onto.load()

with onto:
    class Editor(owl.Thing):
        def introduce(self):
            print('I am {0}'.format(self.personName))

    class Edition(owl.Thing):
        def publish(self):
            print('Published on {0}, no. {1}'.format(self.dateOfPublication, self.editionNumber))

    class Author(owl.Thing):
        def introduce(self):
            print('I am {0}'.format(self.personName))

    class Book(owl.Thing):
        def read(self):

            author_name = ', '.join([a.personName for a in self.writtenBy])
            print('I am reading a {2} book named {0} written by {1}'.format(self.title,
                                                                            author_name,
                                                                            ', '.join(self.genre)))
            editions = self.hasEdition
            for ed in editions:
                ed.publish()
            # edition = onto.Edition(self.hasEdition)
            # edition.publish()


book = onto.Book('book2')
book.read()`
# author = onto.Author('author98')
# author.introduce()
# editor = onto.Editor('editor21')
# editor.introduce()
# edition = onto.Edition('edition21')
# edition.publish()

# novels = onto.search(genre="Horror")
# for novel in novels:
#     novel.read()
