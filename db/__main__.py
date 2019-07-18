import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lxml import etree

from .Base import Base, dbURL, Node, Edge, EdgeTypes


db_engine = create_engine(dbURL)

Base.metadata.create_all(db_engine)

SessionFactory = sessionmaker(bind=db_engine)
session = SessionFactory()

def xpathGetInt(element, path):
    if not path.endswith('text()') and path.endswith('/'):
        path += 'text()'
    else:
        path += '/text()'

    result = element.xpath(path)
    if result:
        return int(result[0])
    else:
        return None


def xpathGetStr(element, path):
    if not path.endswith('text()') and path.endswith('/'):
        path += 'text()'
    else:
        path += '/text()'

    result = element.xpath(path)
    if result:
        return result[0]
    else:
        return None

def addWritings():

    # Get a set of writings from the JMdict
    jmdict_writings = set()
    for event, word in etree.iterparse("./db/JMdict_e.xml", tag="entry"):
        writing = xpathGetStr(word, "k_ele[not(ke_inf/text()='&oK;')]/keb")
        if writing is not None:
            jmdict_writings.add(writing)

    print(len(jmdict_writings))

    # Get a set of writings from the database
    result = session \
            .query(Node) \
            .join(Node.incoming_edges) \
            .filter(Edge.type == EdgeTypes.writing) \
            .all()
    db_writings = set([writing.content for writing in result])

    print(len(db_writings))

    # Get the difference, to know which writings to add
    new_writings = jmdict_writings - db_writings

    print(len(new_writings))

    # Add the writings, and mark them as such with an Edge
    insert = []
    for writing in new_writings:
        new_node = Node(uuid=uuid.uuid4(), content=writing)
        new_edge = Edge(source_uuid=new_node.uuid, target_uuid=new_node.uuid, type=EdgeTypes.writing)
        insert.append(new_node)
        insert.append(new_edge)
    session.bulk_save_objects(insert)
    session.commit()

addWritings()

