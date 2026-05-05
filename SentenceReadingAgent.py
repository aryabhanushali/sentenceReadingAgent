import re
class SentenceReadingAgent:
    def __init__(self):
        # Initialize any instance variables if needed
        pass



    def solve(self, sentence, question):
        # name list
        names = {'serena','andrew','bobbie','cason','david','farzana','frank','hannah','ida','irene','jim','jose','keith','laura','lucy',
            'meredith','nick','ada','yeeling','yan'}

        det = {'a','an','the','this','that','these','those','my','your','his','her','its','our','their','every','each','some','any','no'}

        aux = {'is','are','was','were','be','been','being','do','does','did','have','has','had','will','would','can','could','may','might','shall','should','must','am'}

        preps = {'to','from','in','on','at','by','for','with','about','of','into','onto','near','over','under','through','between',
            'after','before','during','around','down','up','toward','beside','behind','across','against','along','among'}

        verb_map = {
            'brought':'bring','brings':'bring',
            'went':'go','goes':'go','gone':'go',
            'walked':'walk','walks':'walk',
            'ran':'run','runs':'run',
            'took':'take','takes':'take','taken':'take',
            'gave':'give','gives':'give','given':'give',
            'drove':'drive','drives':'drive',
            'rode':'ride','rides':'ride',
            'flew':'fly','flies':'fly',
            'played':'play','plays':'play',
            'talked':'talk','talks':'talk',
            'traveled':'travel','travels':'travel',
            'started':'start','starts':'start',
            'made':'make','makes':'make',
            'told':'tell','tells':'tell'
        }

        location_words = {'school','home','house','room','park','store','market','library','hospital','office',
            'church','gym','bank','shop','city','town','farm','field','road','street','beach','lake',
            'pool','yard','garden','north','south','east','west','center','forest','mountain','river',
            'sea','island','car','boat','bus','train','plane','ship'
        }

        dist_words = {'mile','miles','feet','foot','yard','yards','block','blocks','step','steps'}

        adj_words = {'short','long','big','small','large','little','great','good','bad','new','old','high','low',
            'fast','slow','hard','soft','hot','cold','warm','cool','early','late','dark','light','young',
            'quick','strong','deep','dry','wet','heavy','thin','thick','wide','bright','loud','quiet',
            'clean','fresh','sweet','red','blue','green','black','white','yellow','orange','purple',
            'pink','brown','gold','gray','full','free','first','last','next','same','few','half',
            'fine','rich','poor','all'
        }

        time_words = {'morning','afternoon','evening','night','noon','midnight','today','yesterday',
            'tomorrow','early','late','soon','now','then','later','before','after'}

        def normalize(w):
            lw = w.lower()
            if lw in verb_map:
                return verb_map[lw]
            return lw

        def is_time(w):
            return bool(re.match(r'^\d{1,2}:\d{2}(am|pm)?$', w.lower()))

        def is_name(w):
            return w.lower() in names

        def tokenize(text):
            text = text.strip()
            if text and text[-1] in '.?':
                text = text[:-1]
            return text.split()

        s_tok = tokenize(sentence)
        q_tok = tokenize(question)
        s_low = [x.lower() for x in s_tok]
        q_low = [x.lower() for x in q_tok]

        if not q_low:
            return ""

        qw = q_low[0]
        q_names = [w for w in q_tok if is_name(w)]
        s_names = [w for w in s_tok if is_name(w)]

        if qw == "when" or (qw == "at" and "time" in q_low):
            for w in s_tok:
                if is_time(w):
                    return w
            for i in range(len(s_low)):
                if s_low[i] in time_words:
                    return s_tok[i]
            return ""

        if qw == "who":

            if "with" in q_low:
                if "and" in s_low:
                    idx = s_low.index("and")
                    asked = q_names[0].lower() if q_names else None
                    before = s_tok[idx-1] if idx > 0 else None
                    after = s_tok[idx+1] if idx+1 < len(s_tok) else None
                    if before and is_name(before) and before.lower() != asked:
                        return before
                    if after and is_name(after) and after.lower() != asked:
                        return after

                if "with" in s_low:
                    wi = s_low.index("with")
                    j = wi+1
                    while j < len(s_low) and s_low[j] in det:
                        j += 1
                    if j < len(s_low):
                        return s_tok[j]

            obj_pronouns = {'us','me','him','them','her'}

            if q_low[-1] == "to" or ("to" in q_low and q_low.index("to") > len(q_low)//2):
                to_idx = None
                for qi,qw2 in enumerate(q_low):
                    if qw2 == "to" and qi+1 < len(q_low) and is_name(q_low[qi+1]):
                        to_idx = qi
                        break

                if to_idx is not None:
                    pass
                else:
                    for i,w in enumerate(s_low):
                        if w == "to" and i+1 < len(s_low):
                            nxt = s_low[i+1]
                            if nxt in det and i+2 < len(s_low) and is_name(s_low[i+2]):
                                return s_tok[i+2]
                            if is_name(nxt) or nxt in obj_pronouns:
                                return s_tok[i+1]

                    for i,st in enumerate(s_low):
                        if i+1 < len(s_low) and s_low[i+1] in obj_pronouns:
                            if st not in aux and st not in det and st not in preps:
                                return s_tok[i+1]

                    give_verbs = {'give','gave','gives','given','send','sent','sends','show','showed','shows',
                        'shown','tell','told','tells','teach','taught','teaches','bring','brought','brings',
                        'lend','pass','passed','passes','offer','offered'}
                    for i,w in enumerate(s_low):
                        if w in give_verbs:
                            j = i+1
                            while j < len(s_low) and s_low[j] in det:
                                j += 1
                            if j < len(s_low) and (is_name(s_low[j]) or s_low[j] in obj_pronouns):
                                return s_tok[j]

            q_content = [t for t in q_low
                if t not in aux and t not in det and t not in preps
                and not is_name(t)
                and t not in {"who","what","where","when","how","why","which","and","or","did","does","do"}]

            subj_pronouns = {'she','he','they','we','i','you','it'}
            for qv in q_content:
                for i,st in enumerate(s_low):
                    if normalize(st) == normalize(qv):
                        j = i-1
                        while j >= 0:
                            if is_name(s_low[j]) or s_low[j] in subj_pronouns:
                                return s_tok[j]
                            if s_low[j] in preps or s_low[j] in aux:
                                break
                            j -= 1

            asked = {n.lower() for n in q_names}
            for n in s_names:
                if n.lower() not in asked:
                    return n
            if s_names:
                return s_names[0]

            for i,w in enumerate(s_low):
                if w in aux or w in verb_map or normalize(w) != w:
                    for j in range(i-1, -1, -1):
                        if s_low[j] not in det and s_low[j] not in preps and s_low[j] not in aux:
                            return s_tok[j]
                    break

            return ""

        if qw == "what":

            color_words = {'red','blue','green','black','white','yellow','orange','purple','pink','brown','gray','gold','dark','light'}

            if "name" in q_low:
                for w in s_tok:
                    if is_name(w):
                        return w
                for i,w in enumerate(s_tok):
                    if i > 0 and w[0].isupper():
                        return w

            if len(q_low) == 3 and q_low[1] in aux and q_low[2] in adj_words:
                target_adj = q_low[2]
                for i,w in enumerate(s_low):
                    if w == target_adj:
                        j = i-1
                        while j >= 0 and s_low[j] in (aux | {'very','really','quite','so'}):
                            j -= 1
                        while j >= 0 and s_low[j] in preps:
                            j -= 1
                            while j >= 0 and s_low[j] not in preps and s_low[j] not in (aux|det):
                                j -= 1
                            j += 1
                            break
                        while j >= 0 and s_low[j] in det:
                            j -= 1
                        if j >= 0 and s_low[j] not in (aux | det | preps):
                            k = 0
                            while k < len(s_low) and s_low[k] in det:
                                k += 1
                            if k < i and s_low[k] not in (aux | preps):
                                return s_tok[k]

            if len(q_low) > 1 and q_low[1] in ("color","colour","size","kind","shape"):
                word_set = color_words if ("color" in q_low[1] or "colour" in q_low[1]) else adj_words
                q_noun = None
                for t in reversed(q_low[2:]):
                    if t not in aux and t not in det:
                        q_noun = t
                        break
                if q_noun and q_noun in s_low:
                    ni = s_low.index(q_noun)
                    j = ni-1
                    while j >= 0:
                        if s_low[j] in det:
                            j -= 1
                            continue
                        if s_low[j] in word_set:
                            return s_tok[j]
                        break
                for i,w in enumerate(s_low):
                    if w in word_set:
                        return s_tok[i]

            subject_pronouns = {'she','he','it','they','we','i','you'}
            q_content = [t for t in q_low
                if t not in aux and t not in det and t not in preps
                and not is_name(t)
                and t not in {"who","what","where","when","how","why","which","and","or","did","does","do"}
                and t not in subject_pronouns]

            q_content.sort(key=lambda t: 0 if t in verb_map or normalize(t) != t else 1)

            for qv in q_content:
                for i,st in enumerate(s_low):
                    if normalize(st) == normalize(qv):

                        j = i+1
                        while j < len(s_low) and s_low[j] in det:
                            j += 1

                        if j < len(s_low) and s_low[j] not in preps:
                            indirect = {'her','him','me','us','them','you','it'}
                            if s_low[j] in indirect or is_name(s_low[j]):
                                j += 1
                                while j < len(s_low) and s_low[j] in det:
                                    j += 1

                            if (j < len(s_low) and s_low[j] not in adj_words
                                    and j+1 < len(s_low) and s_low[j+1] in det):
                                j += 1
                                while j < len(s_low) and s_low[j] in det:
                                    j += 1

                            if j < len(s_low) and s_low[j] not in preps:
                                if s_low[j] in adj_words and j+1 < len(s_low):
                                    return s_tok[j] + " " + s_tok[j+1]
                                return s_tok[j]

                        if j < len(s_low) and s_low[j] in preps:
                            k = j+1
                            while k < len(s_low) and s_low[k] in det:
                                k += 1
                            if k < len(s_low) and s_low[k] not in q_low:
                                return s_tok[k]

                        j = i-1
                        while j >= 0 and s_low[j] in (aux | det):
                            j -= 1
                        if j >= 0 and s_low[j] not in preps:
                            return s_tok[j]

            return ""

        if qw == "where":
            for i,w in enumerate(s_low):
                if w == "to" and i+1 < len(s_low):
                    nxt = s_low[i+1]
                    if normalize(nxt) == "go" and i+2 < len(s_low) and s_low[i+2] == "to":
                        if i+3 < len(s_low) and s_low[i+3] in location_words:
                            return s_tok[i+3]
                        continue
                    if nxt in aux or nxt in verb_map:
                        continue
                    if nxt in det:
                        if i+2 < len(s_low) and s_low[i+2] in location_words:
                            return s_tok[i+2]
                    elif nxt in location_words:
                        return s_tok[i+1]

            be_verbs = {"is","are","was","were"}
            for i,w in enumerate(s_low):
                if w in be_verbs and i+1 < len(s_low):
                    j = i+1
                    while j < len(s_low) and s_low[j] in det:
                        j += 1
                    if j < len(s_low) and s_low[j] in location_words and s_low[j] != s_low[0].lower():
                        return s_tok[j]

            for prep in ("at","in","on","near"):
                if prep in s_low:
                    pi = s_low.index(prep)
                    j = pi+1
                    while j < len(s_low) and s_low[j] in det:
                        j += 1
                    if j < len(s_low) and s_low[j] in location_words:
                        return s_tok[j]

            for i,w in enumerate(s_low):
                if w in location_words:
                    return s_tok[i]

            return ""

        if qw == "how":
            if len(q_low) < 2:
                return ""
            how2 = q_low[1]

            if how2 in adj_words:
                if how2 in s_low:
                    return s_tok[s_low.index(how2)]
                q_noun = None
                for t in reversed(q_low[2:]):
                    if t not in aux and t not in det:
                        q_noun = t
                        break
                if q_noun and q_noun in s_low:
                    ni = s_low.index(q_noun)
                    j = ni-1
                    while j >= 0:
                        if s_low[j] in det:
                            j -= 1
                            continue
                        if s_low[j] in adj_words:
                            return s_tok[j]
                        break
                be_verbs = {"is","are","was","were","be","been"}
                for i,w in enumerate(s_low):
                    if w in be_verbs and i+1 < len(s_low):
                        j = i+1
                        while j < len(s_low) and s_low[j] in {"very","really","quite","so"}:
                            j += 1
                        if j < len(s_low) and s_low[j] in adj_words and s_low[j] != how2:
                            return s_tok[j]
                for i,w in enumerate(s_low):
                    if w in adj_words and w != how2 and w not in det:
                        return s_tok[i]

            elif how2 == "far":
                nums = {'one','two','three','four','five','six','seven','eight','nine','ten','half'}
                for i,w in enumerate(s_low):
                    if w in dist_words:
                        if i > 0 and s_low[i-1] in nums:
                            return s_tok[i-1] + " " + s_tok[i]
                        return s_tok[i]

            elif how2 in ("many","much"):
                num_words = {'one','two','three','four','five','six','seven','eight','nine','ten',
                    'hundred','thousand','some','few','several','half','all'}
                for i,w in enumerate(s_low):
                    if w in num_words:
                        if i+1 < len(s_low) and s_low[i+1] in {'hundred','thousand','million'}:
                            return s_tok[i] + " " + s_tok[i+1]
                        return s_tok[i]

            elif how2 == "often":
                for i,w in enumerate(s_low):
                    if w in {'every','always','never','often','sometimes','once','twice','usually'}:
                        return s_tok[i]

            elif how2 in ("do","does","did"):
                manner = {'walk','walked','walks','run','ran','runs','drive','drove','drives',
                    'fly','flew','flies','swim','swam','ride','rode','travel','traveled',
                    'skip','jump','climb','crawl'}
                for i,w in enumerate(s_low):
                    if w in manner:
                        return s_tok[i]
                ignore = {'go','went','goes','get','got','come','came','is','are','was','were','have','has','had','be','been'}
                for i,w in enumerate(s_low):
                    if (w not in ignore and w not in aux and w not in det and w not in preps
                            and not is_name(w) and w not in {'and','or','when','there','no','not'}
                            and not is_time(w)):
                        return s_tok[i]

            return ""

        if qw == "why":
            for conj in ('because','since','so'):
                if conj in s_low:
                    ci = s_low.index(conj)
                    j = ci+1
                    while j < len(s_low) and s_low[j] in det:
                        j += 1
                    skip_why = {'it','he','she','they','we','i','you','is','are','was','were','be','been','very','so','quite'}
                    while j < len(s_low) and s_low[j] in skip_why:
                        j += 1
                    if j < len(s_low):
                        return s_tok[j]
            return ""

        if qw == "which":
            if len(q_low) >= 4 and q_low[-1] in adj_words:
                target = q_low[-1]
                for i,w in enumerate(s_low):
                    if w == target:
                        return s_tok[i]
            q_noun = None
            for t in q_low[1:]:
                if t not in aux and t not in det and t not in preps and t not in {'which','is','are','was','were'}:
                    q_noun = t
                    break
            if q_noun and q_noun in s_low:
                ni = s_low.index(q_noun)
                j = ni-1
                while j >= 0 and s_low[j] in det:
                    j -= 1
                if j >= 0 and s_low[j] in adj_words:
                    return s_tok[j]
            return ""

        skip = aux | det | preps
        for qw_content in q_low:
            if qw_content not in skip:
                base = normalize(qw_content)
                for i,st in enumerate(s_low):
                    if normalize(st) == base:
                        if i+1 < len(s_tok):
                            return s_tok[i+1]

        return ""