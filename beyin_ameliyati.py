import torch

# //[EK] ZIRH BYPASS (Halı Bombardımanı)
for i in range(1, 8):
    if not hasattr(torch, f"int{i}"):
        setattr(torch, f"int{i}", torch.int8)
    if not hasattr(torch, f"uint{i}"):
        setattr(torch, f"uint{i}", torch.uint8)

from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

max_seq_length = 2048
print("⏳ Karargah: Llama 3 (8B) beyni ameliyat masasına yatırılıyor...")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-Instruct-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = None,
    load_in_4bit = True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

from unsloth.chat_templates import get_chat_template
tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3",
    mapping = {"role" : "role", "content" : "content", "user" : "user", "assistant" : "assistant"}
)

def formatting_prompts_func(examples):
    convos = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False) for convo in convos]
    return { "text" : texts, }

dataset = load_dataset("json", data_files="/mnt/c/Users/Hasan Doğan/sohbet/egitim_verisi.jsonl", split="train")
dataset = dataset.map(formatting_prompts_func, batched = True,)

print("⚔️ Karargah: Eğitim (Fine-Tuning) Taarruzu Başlıyor!")

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 100,
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        save_strategy = "no",
    ),
)

trainer_stats = trainer.train()

print("✅ Karargah: Eğitim Tamamlandı. Zeka garanti altına alınıyor (Can Yeleği)...")
# //[EK] CAN YELEĞİ: 16 GB indirme başlamadan önce, emeğimiz çöp olmasın diye 40 MB'lık saf zekayı anında diske yazıyoruz!
model.save_pretrained("/mnt/c/Users/Hasan Doğan/sohbet/AYZERS_v1_LORA")
tokenizer.save_pretrained("/mnt/c/Users/Hasan Doğan/sohbet/AYZERS_v1_LORA")
print("🛡️ Can Yeleği aktif! Zeka diske kaydedildi. Şimdi ana gövde indiriliyor ve GGUF paketleniyor...")

# //[EK] Devasa indirme ve Ollama paketlemesi şimdi başlıyor. Çökse bile zekamız 'AYZERS_v1_LORA' klasöründe güvende.
model.save_pretrained_gguf("/mnt/c/Users/Hasan Doğan/sohbet/AYZERS_v1", tokenizer, quantization_method = "q4_k_m")

print("🚀 GÖREV TAMAMLANDI: AYZERS_v1 klasörü ve GGUF dosyası Windows dizininde kullanıma hazır!")
