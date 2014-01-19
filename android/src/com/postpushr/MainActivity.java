package com.postpushr;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Toast;

import com.postpushr.fragments.AddPostcardFragment;
import com.postpushr.fragments.AddPostcardFragment.AccountHolder;
import com.postpushr.fragments.HomeFragment;
import com.postpushr.fragments.HomeFragment.PostcardFlowListener;
import com.postpushr.fragments.LoginFragment;
import com.postpushr.fragments.RegisterFragment;
import com.postpushr.fragments.SignInFragment;
import com.postpushr.fragments.SignInFragment.SignInListener;
import com.postpushr.model.Account;

public class MainActivity extends Activity implements AccountHolder, SignInListener, PostcardFlowListener {

	private Account mAccount;

	@Override
	protected void onSaveInstanceState(Bundle outState) {

		boolean home = (getFragmentManager().findFragmentById(R.id.fragment_container) instanceof HomeFragment);
		outState.putBoolean("HOME", home);

		super.onSaveInstanceState(outState);
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		mAccount = null;
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		// getFragmentManager().beginTransaction().add(R.id.fragment_container,
		// new SignInFragment()).commit();

		if (savedInstanceState != null && savedInstanceState.getBoolean("HOME") == false) {
			switchToAddPostcardFragment();
		} else {
			getFragmentManager().beginTransaction().add(R.id.fragment_container, new SignInFragment()).commit();
			// moveToHomeFragment(getAccount());
		}
	}

	@Override
	public void switchToLoginFragment() {
		getFragmentManager().beginTransaction().replace(R.id.fragment_container, new LoginFragment()).addToBackStack("Replace with LoginFragment")
				.commit();
	}

	@Override
	public void switchToRegisterFragment() {
		getFragmentManager().beginTransaction().replace(R.id.fragment_container, new RegisterFragment())
				.addToBackStack("Replace with RegisterFragment").commit();
	}

	// TODO: implement validation in the original caller
	@Override
	public void moveToHomeFragment(Account account) {
		mAccount = account;
		HomeFragment homeFragment = new HomeFragment();
		getFragmentManager().beginTransaction().replace(R.id.fragment_container, homeFragment).commit();
		homeFragment.setListAdapter(homeFragment.new OrderListAdapter(this, mAccount));

	}

	@Override
	public void executePostcardCameraIntent() {
		Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
		/*
		 * Uri fileUri = getOutputImageFileUri(getPostcardCode());
		 * intent.putExtra(MediaStore.EXTRA_OUTPUT, fileUri);
		 */
		startActivityForResult(intent, getPostcardCode());
	}

	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		if (resultCode == RESULT_OK) {
			// Image captured and saved to fileUri specified in the Intent
			// Toast.makeText(this, "Image saved to:\n" + data.getData(),
			// Toast.LENGTH_LONG).show();
			((AddPostcardFragment) getFragmentManager().findFragmentById(R.id.fragment_container)).setPictureFilename(data.getData());
			if (requestCode == getPostcardCode()) {

			} else {

			}
		} else if (resultCode == RESULT_CANCELED) {
			// User cancelled the image capture
		} else {
			Toast.makeText(this, "Could not capture image", Toast.LENGTH_LONG).show();
		}
	}

	@Override
	public int getPostcardCode() {
		return 1;
	}

	@Override
	public int getSelfieCode() {
		return 2;
	}

	private Uri getOutputImageFileUri(int type) {
		return Uri.fromFile(getOutputMediaFile(type));
	}

	/** Create a File for saving an image or video */
	private File getOutputMediaFile(int type) {
		int index = 0;

		System.err.println("DEBUGG:" + index++);
		if (Environment.getExternalStorageState() == Environment.MEDIA_MOUNTED) {
			System.err.println("DEBUGG:" + index++);
			File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES), "PostPushr");
			System.err.println("DEBUGG:" + index++);

			// Create the storage directory if it does not exist
			if (!mediaStorageDir.exists()) {
				if (!mediaStorageDir.mkdirs()) {
					Log.d("PostPushr", "failed to create directory");
					return null;
				}
			}
			System.err.println("DEBUGG:" + index++);

			// Create a media file name
			String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
			File mediaFile;
			System.err.println("DEBUGG:" + index++);

			if (type == getPostcardCode()) {
				mediaFile = new File(mediaStorageDir.getPath() + File.separator + "Postcard_" + timeStamp + ".jpg");
				/*
				 * } else if (type == getSelfieCode()) { mediaFile = new
				 * File(mediaStorageDir.getPath() + File.separator + "Selfie_" +
				 * timeStamp + ".mp4");
				 */} else {
				return null;
			}

			return mediaFile;
		}
		return null;
	}

	@Override
	public void switchToAddPostcardFragment() {
		getFragmentManager().beginTransaction().replace(R.id.fragment_container, new AddPostcardFragment())
				.addToBackStack("Replace with AddPostcardFragment").commit();

	}

	@Override
	public Account getAccount() {
		return new Account("zhangd@mit.edu", "8hfybuxm", null);
	}
}
