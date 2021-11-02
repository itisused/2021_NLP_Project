# prediction할 때 src 데이터로 텍스트 파일이 들어가는데 이걸 코드 내에서 string으로 받아서 prediction 을 해보자!
from onmt.translate.translator import build_translator
from argparse import Namespace
import sentencepiece as spm

def translator(sentence):
    kor_tokenizer = spm.SentencePieceProcessor()
    kor_model_prefix = './static/model/subword_kor'
    kor_tokenizer.Load(kor_model_prefix + '.model')

    eng_tokenizer = spm.SentencePieceProcessor()
    eng_model_prefix = './static/model/subword_eng'
    eng_tokenizer.Load(eng_model_prefix + '.model')

    model_path = './static/model/'
    opt = Namespace(models=[model_path + 'model_step_200000.pt'], n_best=1, alpha=0.0, batch_type='tokens', beam_size=5, beta=-0.0, block_ngram_repeat=0, coverage_penalty='none', data_type='text', dump_beam='', fp32=False, int8=False, gpu=-1, ignore_when_blocking=[], length_penalty='none', max_length=100, max_sent_length=None, min_length=0, output='/dev/null', phrase_table='', random_sampling_temp=1.0, random_sampling_topk=0, random_sampling_topp=0, ratio=-0.0, replace_unk=False, ban_unk_token=False, tgt_prefix=False, report_align=False, report_time=False, seed=829, stepwise_penalty=False, tgt=None, verbose=False)
    translator = build_translator(opt, report_score=False)

    tokens = kor_tokenizer.encode_as_pieces(sentence)
    sentence = " ".join(tokens)
    translated = translator.translate([sentence], batch_size=1)
    detokenized = eng_tokenizer.decode_pieces(translated[1][0][0].split())
    return detokenized