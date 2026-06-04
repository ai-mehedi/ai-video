"""
RunPod Serverless handler for DubStudio.

Input job:
  { "video_url": "...", "target_lang": "bn", "num_speakers": 2, "lipsync": false,
    "result_put_url": "<S3 presigned PUT url, optional>" }

Output:
  { "result_url": "<presigned GET or the PUT url>" }  or  { "error": "..." }

Local test (no RunPod):
  python handler.py path/to/video.mp4 bn
"""
import os, sys, tempfile, traceback, urllib.request
import requests
import pipeline


def _download(url, out):
    urllib.request.urlretrieve(url, out)
    return out

def _upload_put(path, put_url):
    with open(path, "rb") as f:
        r = requests.put(put_url, data=f, headers={"Content-Type": "video/mp4"}, timeout=600)
    r.raise_for_status()
    return put_url.split("?")[0]   # the object URL without the signature


def process(job_input):
    work = tempfile.mkdtemp(prefix="job_")
    video = os.path.join(work, "input.mp4")
    _download(job_input["video_url"], video)

    result = pipeline.run_pipeline(
        video_path=video,
        target_lang=job_input["target_lang"],
        num_speakers=job_input.get("num_speakers"),
        lipsync=bool(job_input.get("lipsync", False)),
        work_dir=work,
    )

    put_url = job_input.get("result_put_url")
    if put_url:
        return {"result_url": _upload_put(result, put_url)}
    return {"result_path": result}   # local mode


# ---- RunPod serverless entry ----
def handler(event):
    try:
        return process(event["input"])
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}


if __name__ == "__main__":
    # Local test mode:  python handler.py video.mp4 bn
    if len(sys.argv) >= 3:
        out = pipeline.run_pipeline(sys.argv[1], sys.argv[2])
        print("\n✅ Dubbed video:", out)
    else:
        # RunPod mode
        import runpod
        runpod.serverless.start({"handler": handler})
