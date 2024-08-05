from pathlib import Path

import attr
import lingpy as lp
from clldutils.misc import slug
from pylexibank import Concept
from pylexibank import Dataset as BaseDataset


@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "zhivlovobugrian"
    writer_options = dict(keep_languages=False, keep_parameters=False)

    concept_class = CustomConcept

    def cmd_makecldf(self, args):

        concepts = {}
        wl = lp.Wordlist(self.raw_dir.joinpath("OUG.csv").as_posix())

        for concept in self.conceptlists[0].concepts.values():
            idx = "{0}_{1}".format(concept.number, slug(concept.english))
            args.writer.add_concept(
                ID=idx,
                Number=concept.number,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concepts[concept.english] = idx
        concepts["bite (V)"] = concepts["bite"]
        concepts["burn (V)"] = concepts["burn tr."]
        concepts["claw"] = concepts["claw (nail)"]
        concepts["come (V)"] = concepts["come"]
        concepts["die (V)"] = concepts["die"]
        concepts["drink (V)"] = concepts["drink"]
        concepts["eat (V)"] = concepts["eat"]
        concepts["fat"] = concepts["fat n."]
        concepts["fly (V)"] = concepts["fly v."]
        concepts["give (V)"] = concepts["give"]
        concepts["hear (V)"] = concepts["hear"]
        concepts["kill (V)"] = concepts["kill"]
        concepts["know (V)"] = concepts["know"]
        concepts["lie (V)"] = concepts["lie"]
        concepts["rain (V)"] = concepts["rain"]
        concepts["say (V)"] = concepts["say"]
        concepts["see (V)"] = concepts["see"]
        concepts["sit (V)"] = concepts["sit"]
        concepts["sleep (V)"] = concepts["sleep"]
        concepts["stand (V)"] = concepts["stand"]
        concepts["swim (V)"] = concepts["swim"]
        concepts["warm (hot)"] = concepts["warm"]
        concepts["walk (go)"] = concepts["walk(go)"]
        languages = args.writer.add_languages(
            lookup_factory="Name", id_factory=lambda x: slug(x["Name"])
        )

        args.writer.add_sources()
        for idx in wl:
            lexeme = args.writer.add_form(
                Language_ID=languages[wl[idx, "language"]],
                Parameter_ID=concepts[wl[idx, "concept"]],
                Value=wl[idx, "ipa"],
                Form=".".join(wl[idx, "tokens"]).replace("#", "-"),
                # Segments=wl[idx, 'tokens'],
                Source="Zhivlov2011",
                Loan=True if wl[idx, "cogid"] < 0 else False,
            )
            args.writer.add_cognate(
                lexeme=lexeme,
                Cognateset_ID=wl[idx, "cogid"],
                Cognate_Detection_Method="expert",
                Source=["Zhivlov2011"],
            )
