import uuid
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lxml import etree

from .Base import Base, dbURL, Node, Edge, EdgeTypes


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


db_engine = create_engine(dbURL)

Base.metadata.create_all(db_engine)

SessionFactory = sessionmaker(bind=db_engine)


def getReadingFromEntry(entry):
    return entry.xpath("r_ele/reb/text()")[0]

def getWritingFromEntry(entry):
    writing = entry.xpath("k_ele/keb/text()")

    if writing:
        return writing[0]
    else:
        return getReadingFromEntry(entry)

def getWritingSetFromJMdict():
    writings = set()
    for _event, entry in etree.iterparse("./db/JMdict_e.xml", tag="entry"):
        writing = getWritingFromEntry(entry)
        writings.add(writing)

    return writings

def getContentSet(node_set):
    return set([n.content for n in node_set])

def getMatchingNodesQuery(session, match_set):
    return session.query(Node).filter(Node.content.in_(match_set))

def getMatchingNodes(session, match_set):
    return getMatchingNodesQuery(session, match_set).all()

def getMatchingNodesOfType(session, match_set, type):
    return getMatchingNodesQuery(session, match_set) \
            .join(Node.incoming_edges) \
            .filter(Edge.type == type) \
            .all()

def addNodes(session, content_set):
    session.bulk_save_objects([Node(content=content) for content in content_set])

def addReflexiveEdges(session, node_set, type):
    session.bulk_save_objects([Edge(source_uuid=n.uuid, target_uuid=n.uuid, type=type) for n in node_set])

def addWritingNodesForWritingSet(jmdict_writings):
    session = SessionFactory()

    existing_writings = getContentSet(getMatchingNodes(session, jmdict_writings))
    logger.info(str(len(existing_writings)) + " nodes with matching content already existing in database.")

    missing_writings = jmdict_writings - existing_writings

    if missing_writings:
        addNodes(session, missing_writings)

    session.commit()
    logger.info(str(len(missing_writings)) + " nodes added to the database.")

def addWritingEdgesForWritingSet(jmdict_writings):
    session = SessionFactory()

    typed_writings = getContentSet(getMatchingNodesOfType(session, jmdict_writings, EdgeTypes.writing))
    logger.info(str(len(typed_writings)) +
                " writings with Edge of type `writing` found in the database.")

    untyped_writings = jmdict_writings - typed_writings

    if untyped_writings:
        untyped_nodes = getMatchingNodes(session, untyped_writings)
        addReflexiveEdges(session, untyped_nodes, EdgeTypes.writing)

    session.commit()
    logger.info(str(len(untyped_writings)) + " edges added to the database.")


def addWritings():
    jmdict_writings = getWritingSetFromJMdict()
    logger.info(str(len(jmdict_writings)) + " writings found in JMdict.")

    addWritingNodesForWritingSet(jmdict_writings)
    addWritingEdgesForWritingSet(jmdict_writings)

addWritings()
